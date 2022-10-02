(() => {
    // src/index.js
    blacklist = [];
    whitelist = ["^https://maxsimmonds.engineer$"];
    function isListed(uri, listing) {
      var ret = false;
      if (typeof uri == "string") {
        listing.forEach((m) => {
          if (uri.match(m) != null)
            ret = true;
        });
      } else {
        ret = true;
      }
      return ret;
    }
    addEventListener("fetch", async (event) => {
      event.respondWith(async function() {
        isOPTIONS = event.request.method == "OPTIONS";
        var origin_url = new URL(event.request.url);
        function fix(myHeaders2) {
          myHeaders2.set("Access-Control-Allow-Origin", event.request.headers.get("Origin"));
          if (isOPTIONS) {
            myHeaders2.set("Access-Control-Allow-Methods", event.request.headers.get("access-control-request-method"));
            acrh = event.request.headers.get("access-control-request-headers");
            if (acrh) {
              myHeaders2.set("Access-Control-Allow-Headers", acrh);
            }
            myHeaders2.delete("X-Content-Type-Options");
          }
          return myHeaders2;
        }
        var fetch_url = decodeURIComponent(decodeURIComponent(origin_url.search.substr(1)));
        var orig = event.request.headers.get("Origin");
        var remIp = event.request.headers.get("CF-Connecting-IP");
        if (!isListed(fetch_url, blacklist) && isListed(orig, whitelist)) {
          xheaders = event.request.headers.get("x-cors-headers");
          if (xheaders != null) {
            try {
              xheaders = JSON.parse(xheaders);
            } catch (e) {
            }
          }
          if (origin_url.search.startsWith("?")) {
            recv_headers = {};
            for (var pair of event.request.headers.entries()) {
              if (pair[0].match("^origin") == null && pair[0].match("eferer") == null && pair[0].match("^cf-") == null && pair[0].match("^x-forw") == null && pair[0].match("^x-cors-headers") == null)
                recv_headers[pair[0]] = pair[1];
            }
            if (xheaders != null) {
              Object.entries(xheaders).forEach((c) => recv_headers[c[0]] = c[1]);
            }
            newreq = new Request(event.request, {
              "redirect": "follow",
              "headers": recv_headers
            });
            var response = await fetch(fetch_url, newreq);
            var myHeaders = new Headers(response.headers);
            cors_headers = [];
            allh = {};
            for (var pair of response.headers.entries()) {
              cors_headers.push(pair[0]);
              allh[pair[0]] = pair[1];
            }
            cors_headers.push("cors-received-headers");
            myHeaders = fix(myHeaders);
            myHeaders.set("Access-Control-Expose-Headers", cors_headers.join(","));
            myHeaders.set("cors-received-headers", JSON.stringify(allh));
            if (isOPTIONS) {
              var body = null;
            } else {
              var body = await response.arrayBuffer();
            }
            var init = {
              headers: myHeaders,
              status: isOPTIONS ? 200 : response.status,
              statusText: isOPTIONS ? "OK" : response.statusText
            };
            return new Response(body, init);
          } else {
            var myHeaders = new Headers();
            myHeaders = fix(myHeaders);
            if (typeof event.request.cf != "undefined") {
              if (typeof event.request.cf.country != "undefined") {
                country = event.request.cf.country;
              } else
                country = false;
              if (typeof event.request.cf.colo != "undefined") {
                colo = event.request.cf.colo;
              } else
                colo = false;
            } else {
              country = false;
              colo = false;
            }
            return new Response(
              "CLOUDFLARE-CORS-ANYWHERE\n\nSource:\nhttps://github.com/Zibri/cloudflare-cors-anywhere\n\nUsage:\n" + origin_url.origin + "/?uri\n\nLimits: 100,000 requests/day\n          1,000 requests/10 minutes\n\n" + (orig != null ? "Origin: " + orig + "\n" : "") + "Ip: " + remIp + "\n" + (country ? "Country: " + country + "\n" : "") + (colo ? "Datacenter: " + colo + "\n" : "") + "\n" + (xheaders != null ? "\nx-cors-headers: " + JSON.stringify(xheaders) : ""),
              { status: 200, headers: myHeaders }
            );
          }
        } else {
          return new Response(
            "Create your own cors proxy</br>\n<a href='https://github.com/Zibri/cloudflare-cors-anywhere'>https://github.com/Zibri/cloudflare-cors-anywhere</a></br>\n\nDonate</br>\n<a href='https://paypal.me/Zibri/5'>https://paypal.me/Zibri/5</a>\n",
            {
              status: 403,
              statusText: "Forbidden",
              headers: {
                "Content-Type": "text/html"
              }
            }
          );
        }
      }());
    });
  })();
  //# sourceMappingURL=index.js.map
  