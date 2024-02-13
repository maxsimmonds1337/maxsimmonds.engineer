  // Just some constants
  const LEETCODE_API_ENDPOINT = 'https://cors-proxy.maxsimmonds1337.workers.dev?https://leetcode.com/graphql'
  const GetProgress = `
  query getUserProfile($username: String!) {
    matchedUser(username: $username) {
      username
      submitStats: submitStatsGlobal {
        acSubmissionNum {
          difficulty
          count
          submissions
        }
      }
    }
  }`
      
  const fetchStats = async () => {
      console.log(`Fetching stats from LeetCode API.`)
  
      const init = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
        query: GetProgress,
        variables: {username : "theengineeringoctopus"},
      }),
      }
  
      const response = await fetch(LEETCODE_API_ENDPOINT, init)
      return response.json();
  
  }

function setup() {
    createCanvas(windowWidth, windowHeight);
  }
  
  function drawDebug(x, y, radius) {
      drawingContext.setLineDash([5, 3]);
      noFill()
      stroke('grey')
      circle(x, y, 2*radius)
      
      fill('grey')
      circle(x, y, 4)
      
      line(x, y, x, y - radius)
      
        drawingContext.setLineDash([]);
  
  }
  
  function rotateText(x, y, radius, txt, angle, txtSize) {
    // Comment the following line to hide debug objects
    // drawDebug(x, y, radius)
  
    textFont('Courier New');
    noStroke()

    // Split the chars so they can be printed one by one
    chars = txt.split("")

    // Decide an angle
    charSpacingAngleDeg = angle;

    // https://p5js.org/reference/#/p5/textAlign
    textAlign(CENTER, BASELINE)
    textSize(txtSize)


    // https://p5js.org/reference/#/p5/push
    // Save the current translation matrix so it can be reset
    // before the end of the function
    push()

    // Let's first move to the center of the circle
    translate(x, y)

    // First rotate half back so that middle char will come in the center
    rotate(radians(-chars.length * charSpacingAngleDeg / 2))

    for (let i = 0; i < chars.length; i++) {
        text(chars[i], 0, -radius)

        // Then keep rotating forward per character
        rotate(radians(charSpacingAngleDeg))
    }

    // Reset all translations we did since the last push() call
    // so anything we draw after this isn't affected
    pop()

}


function updateVals(response_json) {

	// const username = response_json.data.matchedUser.username;

  total = response_json.data.matchedUser.submitStats.acSubmissionNum[0].count;

	easy = response_json.data.matchedUser.submitStats.acSubmissionNum[1].count;
  medium = response_json.data.matchedUser.submitStats.acSubmissionNum[2].count;
  hard = response_json.data.matchedUser.submitStats.acSubmissionNum[3].count;
  noLoop()

	// document.getElementById("username").innerHTML = "User: " + username;
	// document.getElementById("total_submissions").innerHTML = "Total Submissions: " + total_submissions;
	// document.getElementById("easy_completed").innerHTML = "'Easy' questions completed: " + easy_completed;
	// document.getElementById("medium_completed").innerHTML = "'Medium' questions completed: " + medium_completed;
	// document.getElementById("hard_completed").innerHTML = "'Hard' questions completed: " + hard_completed;

}
var total = 0
var easy = 0
var hard = 0
var medium = 0
  
function draw() {
  background(255,255,255);
  
  textAlign(CENTER, CENTER);
  noStroke()
  textSize(32);
  textFont('Courier New');
  text("Leetcode stats\nby Max", width/2, 50)
  

  let data = fetchStats()
  data.then(updateVals)
  
  weight = 40
  
  // easy = 22
  // total = 34
  // medium = 10
  // hard = 0
  
  strokeWeight(weight);
  stroke(0,0,0)
  arc(width/2, height/2, 175*2, 175*2, -PI, 2*PI-PI);
  stroke(0,255,0)
  arc(width/2, height/2, 125*2, 125*2, -PI, (2*PI*(easy/total)) - PI);
  stroke(0,0,255)
  arc(width/2, height/2, 75*2, 75*2, -PI, (2*PI*(medium/total)) - PI);
  stroke(255,0,0)
  arc(width/2, height/2, 25*2, 25*2, -PI, (2*PI*(hard/total)) - PI);
  
  textStyle(BOLD);
    
  textToRotate = str(total) + " questions completed"
  rotateText(width/2, height/2, 100*2, textToRotate, 5, 20)
  rotateText(width/2, height/2, 60*2, str(easy) + " Easy", 10, 20)
  rotateText(width/2, height/2, 35*2, str(medium) + " Medium", 12, 20)
  rotateText(width/2, height/2, 10*2, str(hard) + " Hard", 25, 14)
  textAlign(CENTER, CENTER);
  noStroke()
  textSize(32);
  textFont('Courier New');

}