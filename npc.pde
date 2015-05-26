class Npc
{
  final int BASE_DIAMETER = 10;
  int diameter;
  PVector location;//processing.org/reference/PVector
  PVector velocity;
  color shade;
  int level;
  
  /**
  * Default Npc (no-args)
  */
  Npc()
  {
    diameter = BASE_DIAMETER;
    location = new PVector(10.0,10.0);
    velocity = new PVector(1.0,1.0);
    setShade();
  }
  
  /**
  * The utilized constructor, velocity is calculated based on inputted level
  */
  Npc(int l)
  {
    diameter = BASE_DIAMETER * l;
    level = l;
    location = new PVector(10.0 * l, 10.0 * l);
    velocity = new PVector(calcVelocity(),calcVelocity());
    setShade();
  }
  
  /**
  * Constructor for testing, allows inputted location and velocity
  */
  Npc(int l, PVector loc, PVector v)
  {
    diameter = BASE_DIAMETER * l;
    location = loc;
    if(loc.x < diameter)
      location.x = diameter;
    if(loc.y < diameter);
      location.y = diameter;
    velocity = v;
    setShade();
  }
  
  /**
  * Returns initial velocity calculated according to level
  * (higher level gets lower initial velocity)
  */
  float calcVelocity()
  {
    return 1.2 - ((float)level/5);
  }
  
  /**
  * Sets shade based on Npc size
  * (larger size gets darker color
  */
  void setShade()
  {
    if(diameter <= 255)
      shade = color(255 - (diameter * 5));
    else
      shade = color(255,0,0);
  }
  
  /**
  * Move Npc, responsible for collisions with walls
  */
  void move()
  {
    location.x += velocity.x;
    location.y += velocity.y;
    if(location.x - (diameter / 2) < 0 || location.x + (diameter / 2) > width)
      velocity.x *= -1;
    if(location.y - (diameter / 2) < 0 || location.y + (diameter / 2) > height)
      velocity.y *= -1;
  }
  
  /**
  * Displays the circle
  */
  void display()
  {
    stroke(0);
    fill(shade);
    ellipse(location.x,location.y,diameter,diameter);
  }
  
  int getDiameter()
  {
    return diameter;
  }
  
  int getLevel()
  {
    return level;
  }
  
  String toString()
  {
    return "location = " + location + " velocity = " + velocity;
  }
}
