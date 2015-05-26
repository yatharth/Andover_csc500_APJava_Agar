class Board
{
  int quantity;
  ArrayList<Npc> npcs = new ArrayList<Npc>(quantity);
  Player pl = new Player();
  int score;
  
  /**
  * Constructs a board with an ArrayList of Npcs (quantity q) and
  * creates q many Npcs in that ArrayList
  */
  Board(int q)
  {
    quantity = q;
    distribute();
  }
  
  /**
  * Add quantity Npcs to the npcs 
  */
  void distribute()
  {
    //fill npcs with npcs of random locations
    for(int i = 0; i < quantity; i++)
    {
      addNpc(i);
    }
  }
  
  /**
  * Adds an Npc according to a few restraints: there must always be
  * one level-one Npc, and the new Npc can't overlap in location with
  * any other Npc or the player
  */
  void addNpc(int i)//i = index
  {
    //ensure that at least one Npc is level one
    boolean levelOne = false;
    int c = 0;
    while(!levelOne && c < npcs.size())
    {
      if(npcs.get(c).getLevel() == 1)
        levelOne = true;
      c++;
    }
    int level = 0;
    if(c < npcs.size())//then levelOne = true
    {
      level = (int)random(1,6);
    }
    else
    {
      level = 1;
    }
    //add the actual Npc
    npcs.add(i, new Npc(level));
    int rad = npcs.get(i).getDiameter() / 2;
    PVector loc = new PVector(random(rad,500-rad),random(rad,400-rad));
    //if on top of player
    if(Math.abs(loc.x - pl.location.x) < rad || Math.abs(loc.y - pl.location.y) < rad)
    {
      loc.x = random(rad,500-rad);
      loc.y = random(rad,400-rad);
    }
    npcs.get(i).location = loc;
    
    checkOverlap(i);
  }
  
  /**
  * Ensures that added Npc does not overlap with any others
  */
  void checkOverlap(int i)//i = index
  {
    //j < i because new Npc is always added to the end
    for(int j = 0; j < i; j++)
    {
      float x1 = npcs.get(i).location.x;
      float y1 = npcs.get(i).location.y;
      float x2 = npcs.get(j).location.x;
      float y2 = npcs.get(j).location.y;
      int d1 = npcs.get(i).getDiameter();
      int d2 = npcs.get(j).getDiameter();
      
      if(dist(x1,y1,x2,y2) <= (d1/2) + (d2/2))
      {
        npcs.get(i).location = new PVector(random(0,500),random(0,400));
        checkOverlap(i);
      }
    }
  }
  
  /**
  * All that is necessary to run the game:
  *   Displays/updates players and each Npc
  *   If an eat is possible, eats
  *   Runs collisions
  *   Determines if gameOver
  *   Displays score
  */
  void update()
  {
      pl.display();
      pl.update();
    
    if(score > 200)
      gameOver();
    
    else
    {
      findEat();
      
      for(int i = 0; i < npcs.size(); i++)
      {
        npcs.get(i).display();
        npcs.get(i).move();
      }
      checkCollisions();
      
      scoreDisplay();
    }
  }
  
  /**
  * If an Npc is "touching" another, have them collide obeying
  * elastic collisions (where their level represents their mass)
  */
  void checkCollisions()
  {
    for(int i = 0; i < npcs.size(); i++)
    {
      for(int j = i + 1; j < npcs.size(); j++)
      {
        float x1 = npcs.get(i).location.x;
        float y1 = npcs.get(i).location.y;
        float x2 = npcs.get(j).location.x;
        float y2 = npcs.get(j).location.y;
        int d1 = npcs.get(i).getDiameter();
        int d2 = npcs.get(j).getDiameter();
        
        if(dist(x1,y1,x2,y2) <= (d1/2) + (d2/2))
        {
          float vx1 = npcs.get(i).velocity.x;
          float vy1 = npcs.get(i).velocity.y;
          float vx2 = npcs.get(j).velocity.x;
          float vy2 = npcs.get(j).velocity.y;
          int m1 = npcs.get(i).level;
          int m2 = npcs.get(j).level;
          //reassign velocities
          npcs.get(i).velocity.x = calcVelocity(vx1,vx2,m1,m2);
          npcs.get(i).velocity.y = calcVelocity(vy1,vy2,m1,m2);
          npcs.get(j).velocity.x = calcVelocity(vx2,vx1,m2,m1);
          npcs.get(j).velocity.y = calcVelocity(vy2,vy1,m2,m1);
        }
      }
    }
  }
  
  /**
  * Calculates post-collision velocities according to
  * physical elastic collisions
  */
  float calcVelocity(float v1, float v2, int m1, int m2)
  {
    float fm1 = (float)m1;
    float fm2 = (float)m2;
    return (fm1-fm2)/(fm1+fm2)*v1 + (2*fm2)/(fm1+fm2)*v2;
  }
  
  /**
  * Checks to see if player is "touching" any Npcs
  */
  void findEat()
  {
    for(int i = 0; i < npcs.size(); i++)
    {
      float x1 = npcs.get(i).location.x;
      float y1 = npcs.get(i).location.y;
      float x2 = pl.location.x;
      float y2 = pl.location.y;
      int d1 = npcs.get(i).getDiameter();
      int d2 = pl.getDiameter();
      if(dist(x1,y1,x2,y2) <= (d1/2) + (d2/2))
      {
        eat(npcs.get(i));
      }
    }
  }
  
  /**
  * If player can eat Npc, player eats Npc
  * If Npc can eat player, Npc decreases player
  */
  void eat(Npc other)
  {
    //if player can eat Npc
    if(pl.getDiameter() >= other.getDiameter())
    {
      pl.diameter += other.getLevel();
      npcs.remove(other);
      score += other.getLevel();
      
      //add new one in its place
      addNpc(npcs.size() - 1);
    }
    //if Npc can damage player
    else
    {
      pl.diameter--;
      score--;
      if(pl.diameter < 10)
      {
        pl.diameter = 10;
        score = 0;
      }
    }
  }
  
  /**
  * Displays score
  */
  void scoreDisplay()
  {
    stroke(0);
    fill(0);
    rect(0,0,90,20);
    
    textSize(12);
    fill(255);
    text("Score: " + score, 10,10);
  }
  
  /**
  * Removes Npcs
  * Displays Game Over text
  */
  void gameOver()
  {
    for(int i = 0; i < npcs.size(); i++)
    {
      npcs.remove(i);
    }
    
    //display game over
    textSize(35);
    fill(0);
    text("GAME OVER", 150,200);
  }
}
