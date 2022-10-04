let pixel_slider, input_x_position, input_y_position, pixel_size, board_size; // global vars
let board_size_in_pixels;

class pixel {
  constructor(colour, x, y, size) {
    this.colour = colour;
    this.x = x;
    this.y = y;
    this.height = 0; // this holds the value used for sinewave
    this.size = size;
  }

  ripple(x, phase_shift) {
    if (this.height < 2*3.142) {
      this.height = this.height + x;
    } else {
      this.height = 0;
    }
    this.changeColour(floor(Math.sin(this.height + phase_shift) * 127)+127);
  }

  drawSquare() {
    noStroke();
    square(this.x, this.y, this.size);
  }

  changeColour(newColour) {
    this.colour = newColour;
    fill(this.colour);
    this.drawSquare();
  }

  clearPixel() {
    // this sets the pixel colour to white
    this.changeColour(color("white"));
  }
}
