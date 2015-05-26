class Player
{
  final int BASE_DIAMETER = 10;
  int diameter;
  PVector location;//processing.org/reference/PVector
  PVector velocity;
  
  /**
  * Constructs a player
  */
  Player()
  {
    diameter = 10;
    location = new PVector(250, 200);//start them centered
    velocity = new PVector(0.0, 0.0);
  }
  
  /**
  * Displays the circle
  */
  void display()
  {
    stroke(255,0,0);
    fill(255,0,0);
    ellipse(location.x,location.y,diameter,diameter);
  }
  
  /**
  * Modifies player velocity based on key pressed
  */
  void keyPressed()//http://studio.processingtogether.com/sp/pad/export/ro.9bY07S95k2C2a/latest
  {
    final int k = keyCode;
    
    if((k == LEFT || k == 'A') && location.x > diameter / 2)
      velocity.x = -2;
    if((k == RIGHT || k == 'D') && location.x < width + (diameter / 2))
      velocity.x = 2;
    if((k == UP || k == 'W') && location.y > diameter / 2)
      velocity.y = -2;
    if((k == DOWN || k == 'S') && location.y < height + (diameter / 2))
      velocity.y = 2;
  }
  
  /**
  * Moves the player, responsible for collisions with walls
  */
  void move()//wall interaction help from KarenXia
  {
    if(location.x - (diameter / 2) < 0 && velocity.x < 0 || location.x + (diameter / 2) > width && velocity.x > 0)
      velocity.x = 0;
    if(location.y - (diameter / 2) < 0 && velocity.y < 0 || location.y + (diameter / 2) > height && velocity.y > 0)
      velocity.y = 0;
    location.x += velocity.x;
    location.y += velocity.y;
  }
  
  /**
  * If a key is pressed, move in the manner that the
  * keyPressed and move methods dictate
  */
  void update()
  {
    if(keyPressed == false)
    {
      velocity.x = 0;
      velocity.y = 0;
    }
    else
    {
      keyPressed();
      move();
    }
  }
  
  int getDiameter()
  {
    return diameter;
  }
}
