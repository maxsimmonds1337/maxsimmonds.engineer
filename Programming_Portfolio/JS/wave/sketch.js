var pix_array = [];
const wave_resolution = 3.14 / 100;

function setup() {
  canvas = createCanvas(400, 500);

  board_slider = createSlider(1, 375, 350);
  board_slider.position(10, 100);
  board_slider.style("width", "100px");
  board_slider.input(drawBoard);

  pixel_slider = createSlider(1, 100, 50);
  pixel_slider.position(board_slider.x + 110, board_slider.y);
  pixel_slider.style("width", "100px");
  pixel_slider.input(drawBoard);

  pix_array = drawBoard(); // get a pixel array

}

function draw() {
  background(220);

  fill(color("black")); // this makes the text stay black

  text("Board Size:", board_slider.x, board_slider.y / 2);
  text("Pixel Size:", pixel_slider.x, pixel_slider.y / 2);

  center_of_board = floor(pix_array.length / 2); //use the board center as the epicenter for now

  
  for (let i = 0; i < board_size_in_pixels; i++) {
    for (let j = 0; j < board_size_in_pixels; j++) {
      //colour the middle square black
      let phase_shift = min(abs(center_of_board - i), abs(center_of_board - j));
      pix_array[i][j].ripple(wave_resolution, phase_shift);
    }
  }
}

function drawBoard() {
  let pix_array = [];

  pixel_size = pixel_slider.value(); // get the value of the slider
  board_size = board_slider.value(); // get the value of the slider

  rectMode(CENTER); // all squares referenced to the center

  board_size_in_pixels = board_size / pixel_size; //get the board size in number of pixels

  let board_x = canvas.width / 2 + 1; // this is the x coord of the board center
  let board_y =
    (canvas.height - pixel_slider.y + (canvas.height - pixel_slider.y) / 2) /
      2 +
    10; // this is the y coord of the board center

  // this keeps the grid as central as possible, dynamically
  // this essentially shifts the upper left corner of the grid, relative to the center, by the number of pixels present
  let offset_board_x = board_x - pixel_size * 0.5 * board_size_in_pixels;
  let offset_board_y = board_y - pixel_size * 0.5 * board_size_in_pixels;

  // make a 2D array of pixels, all cleared
  for (let i = 0; i < board_size_in_pixels; i++) {
    pix_array[i] = new Array();
    for (let j = 0; j < board_size_in_pixels; j++) {
      pix_array[i][j] = new pixel(
        color("white"),
        i * pixel_size + offset_board_x,
        j * pixel_size + offset_board_y,
        pixel_size
      );
    }
  }
  return pix_array;
}
