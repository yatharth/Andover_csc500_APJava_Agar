void setup()
{
  size(500,400);
}

Board board = new Board(10);

void draw()
{
  background(255);
  
  board.update();
}
