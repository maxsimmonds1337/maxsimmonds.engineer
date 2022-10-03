let pixel_slider, input_x_position, input_y_position, pixel_size, board_size; // global vars
let pix_array = []; // array to hold the square objects
let board_size_in_pixels;

class pixel {
  constructor(colour, x, y, size) {
    this.colour = colour;
    this.x = x;
    this.y = y;
    this.size = size;      
  }

  drawSquare() {
    square(this.x, this.y, this.size);
  }

  changeColour(newColour) {
    this.colour = newColour;
    fill(this.colour);
    this.drawSquare();
  }
}

function setup() {
  canvas = createCanvas(400, 500);
  
  board_slider = createSlider(1,375,350);
  board_slider.position(10,100);
  board_slider.style('width', '100px');
  board_slider.input(redraw); 
  
  pixel_slider = createSlider(1,100,5);
  pixel_slider.position(board_slider.x + 110, board_slider.y);
  pixel_slider.style('width', '100px');
  pixel_slider.input(redraw); 
  
}

function draw() {
  
  drawBoard();
  
  noLoop();
  
  background(220);
  
  text('Board Size:', board_slider.x, board_slider.y/2);
  text('Pixel Size:', pixel_slider.x, pixel_slider.y/2);
  
  
  for(let i = 0; i<board_size_in_pixels; i++) {
    for(let j = 0; j<board_size_in_pixels; j++) {
     pix_array[i][j].changeColour(color(random(255), random(255), random(255)));
    }
  }
}

function drawBoard() {
  pixel_size = pixel_slider.value(); // get the value of the slider
  board_size = board_slider.value(); // get the value of the slider
  
  rectMode(CENTER); // all squares referenced to the center
  // noStroke();
  
  
  //let board_sqaure = square(200, 300, board_size*pixel_size);
  
  board_size_in_pixels = (board_size/pixel_size); //get the board size in number of pixels
  
  let board_x = canvas.width/2 + 1; // this is the x coord of the board center
  let board_y = (((canvas.height- pixel_slider.y) + ((canvas.height- pixel_slider.y))/2)/2) + 10; // this is the y coord of the board center
  
  
  // this keeps the grid as central as possible, dynamically
  let offset_board_x = board_x-(pixel_size*0.5*board_size_in_pixels); // this essentially shifts the upper left corner of the grid, relative to the center, by the number of pixels present
  let offset_board_y = board_y-(pixel_size*0.5*board_size_in_pixels); // this essentially shifts the upper left corner of the grid, relative to the center, by the number of pixels present

  for(let i = 0; i<board_size_in_pixels; i++) {
    pix_array[i] = new Array ()
    for(let j = 0; j<board_size_in_pixels; j++) {
      pix_array[i][j] = new pixel(color("black"), i*pixel_size+offset_board_x, j*pixel_size+offset_board_y, pixel_size);
      
    }
  }
}