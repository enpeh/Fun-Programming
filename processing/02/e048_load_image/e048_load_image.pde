float x;
PImage photo;

void setup() {
  size(400, 300);
  x = width;
  photo = loadImage("mummo.jpg");
}
void draw() {
  background(0);
  
  image(photo, x, 0);
  
  if(x > 0) {
    x = x - 1;
  }
}
