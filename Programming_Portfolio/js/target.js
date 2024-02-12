function setup() {
    createCanvas(400, 400);
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
  
  function rotateText(x, y, radius, txt) {
      // Comment the following line to hide debug objects
      // drawDebug(x, y, radius)
    
      textFont('Courier New');
      noStroke()
  
      // Split the chars so they can be printed one by one
      chars = txt.split("")
  
      // Decide an angle
      charSpacingAngleDeg = 5;
  
      // https://p5js.org/reference/#/p5/textAlign
      textAlign(CENTER, BASELINE)
      textSize(10)
  
  
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
  
  function draw() {
    background(255,255,255);
    
    textAlign(CENTER, CENTER);
    noStroke()
    textSize(32);
    textFont('Courier New');
    text("Leetcode stats\nby Max", width/2, 50)
    
    weight = 20
    
    var total = 100
    var easy = 10
    var hard = 50
    var medium = 40
    
    textToRotate = str(total) + " total questions"
    textStyle(BOLD);
    rotateText(200, 200, 100, textToRotate)
    textAlign(CENTER, CENTER);
    noStroke()
    textSize(32);
    textFont('Courier New');
    
    strokeWeight(20);
    stroke(0,0,0)
    arc(width/2, height/2, 175, 175, -PI, PI);
    stroke(0,255,0)
    arc(width/2, height/2, 125, 125, -PI, PI*(easy/total));
    stroke(0,0,255)
    arc(width/2, height/2, 75, 75, -PI, PI*(medium/total));
    stroke(255,0,0)
    arc(width/2, height/2, 25, 25, -PI, PI*(hard/total));
    
  
  }