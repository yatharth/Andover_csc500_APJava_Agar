# Agar

Welcome to Agar. Agar is a simple blob game. It's written in [Processing][processing], hence the name [_processed_ algae][agar].
   
Simply run the appropriate launcher in `dist.playforms`.
Too impatient? You can also play [an online version][web] which got [really popular][trends] recently.

You should see a nice initial screen. There is also a nice replay screen. It just happens to be the same.

You are a blob. There are other blobs. You must eat those other blobs to win.

Blobs are colorful. Your blob's ring color shows the color of the largest blob you can eat.

If you hit a smaller blob, you will eat it.
You will grow based on how significant the blob was compared to you.
You can see how far you are to progressing to the next level in the top-left.

If you hit an equally-size blob, you will bounce reflectively.
If you hit a larger blob, you will be eaten.

If you get eaten, you will be berated. You will also shrink.
If you shrink too much, you die.
If you die, you shall spectate the entirety of the grid to reflect on your worth as a human being.

If you're clearly the biggest fish in town, you win!
If you win, you will also get a few extra glorious seconds to enjoy your absolute power.

The grid is much larger than what you can see. You will see enough.
The grid lines should help keep your sanity intact.
If there are multiple players, all will be accommodated.

Oh, did you know you can play with upto 3 other players locally?
Step 1: Make 3 friends.
Step 2: ???
Step 3: Profit!

All of players can move simultaneously in any of the 8 ways it makes sense to move with a 4-way keypad.

There is no AI. Actually, there is an AI, but it has been disabled.
The game is hard enough as it is. You don't want it to be impossible.

You will never spawn over another player. The game will never hang. You will get a nice error message instead.

It's the game of life. And death. Can you do better than randomly-floating blobs?

...

Done? Then you can mod the game! Look for the config file and tinker around.
You'll have to rebuild from source. Use [the Python runner][py] in `libraries` to execute `agar.pyde`.
If you want to export as a launcher, the easiest way to do so is to run the included `build.sh` script.

P.S.: Are a coder? Then have a look at the code! It's short-ish, elegant-ish, and well-ish-documented.
If want to help out, try implementing one of the TODO items. Just make a pull request afterwards. Or email me at <yatharth999@gmail.com> if you don't get (G)it. 

Oh, 'me' is Yatharth Agarwal, BTW. I credit Ava LaRocca's own blob game for the idea to make this clone.

  [trends]: https://www.google.com/trends/explore#q=agar
  [web]: http://agar.io/
  [processing]: https://py.processing.org
  [agar]: https://en.wikipedia.org/wiki/Agar
  [py]: http://py.processing.org/
