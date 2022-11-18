const SLIDER_WIDTH = 14;

function draw_sliders() {
 
  //remove all the peg sliders
  while(peg_sliders.length != 0) {
    
    clear();
    slider = peg_sliders.pop();
    slider.remove();
    
  }
    
  // update the number of pegs slider
  fill("#8901E2");
  text("Number of pegs: " + num_of_pegs_slider.value(), num_of_pegs_slider.x+num_of_pegs_slider.width + 5, num_of_pegs_slider.y + SLIDER_WIDTH)
  
  // make new peg sliders
  for (let i = 0; i < num_of_pegs_slider.value(); i++ ) {
    slider = createSlider(0,100,50);
    slider.position(10,(30+(i*20)));
    slider.input(calculate_gears);
    fill('#8901E2');
    text("Peg " + i + "'s distance from last peg: " + slider.value(),slider.x+slider.width+10, slider.y+SLIDER_WIDTH);
    peg_sliders.push(slider);
    
  } 
  
  calculate_gears();
}

function calculate_gears(){
  
  clear();
  
  // make new peg sliders
  for (let i = 0; i < peg_sliders.length; i++ ) {
    slider = peg_sliders[i];
    fill('#8901E2');
    text("Peg " + i + "'s distance from last peg: " + slider.value(),slider.x+slider.width+10, slider.y+SLIDER_WIDTH);
    
  } 
  
  let pegs = [];
  
  // let pegs = [5,30, 51, 80,105, 130];
  //4, 30, 50
  
  // loop over the peg sliders array
  let cumalative_distance  = 0;
  for (let i = 0; i < peg_sliders.length; i++) {
    console.log(peg_sliders[i].value());
    cumalative_distance += peg_sliders[i].value();
    pegs.push(cumalative_distance);
  }
  console.log(pegs);
  let orig_pegs = pegs.slice();
  let pixel_size = 3;
  
  push();
  
  translate(0, height/2)
  
  let lengths = [];
  let gear_sizes = [];

  let num_of_pegs = pegs.length;
  
  if (num_of_pegs % 2 == 0) {
    gain = 2/3;
  } else {
    gain = 2;
  }
  
  if(num_of_pegs >=2) {
   
    for ( let i = 1; i < num_of_pegs-1; i++ ) {
      pegs[i] = 2*pegs[i];
    }
    
  }

  r0 = 0;
  
  for ( let i = 0; i < num_of_pegs; i++ ) {
  
    if(i % 2 != 0) {
      pegs[i] = gain*pegs[i];
    } else {
      pegs[i] = -gain*pegs[i];
    }
  
    r0 += pegs[i];
  }
  
  
  gear_sizes.push(r0);

  for (let i = 1; i < num_of_pegs-1; i++) {
    gear_sizes.push((orig_pegs[i] - orig_pegs[i-1]) - gear_sizes[i-1])
  }

  gear_sizes.push(gear_sizes[0]/2);
  
  let test = false;
  
  for (let i = 1; i<gear_sizes.length; i++) {
    if (gear_sizes[i] < 1 || gear_sizes[0] < 2) {
      test = true;
    }
  }
  
  if (!test) {
    for(let i=0; i<gear_sizes.length; i++) {
      fill(color('#4CAF50'))
      circle(orig_pegs[i]*pixel_size, 0, gear_sizes[i]*pixel_size*2);
      fill('#000000');
      circle(orig_pegs[i]*pixel_size, 0, 10);
    }
    
  }
  pop();
}

function setup() {
  createCanvas(1000, 600);
}

function draw() {
  
  background(51);

  num_of_pegs_slider = createSlider(0,21,6);
  num_of_pegs_slider.position(10,10);
  num_of_pegs_slider.style('width', width/2 + 'px');
  num_of_pegs_slider.input(draw_sliders);
  
  peg_sliders = []; // this will store array of objects (sliders)
  
  calculate_gears();
  
  noLoop();
}