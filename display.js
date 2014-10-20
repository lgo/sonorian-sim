var c = document.getElementById("left");
var ctx = c.getContext("2d");

height = 512;
width = 512;

draw(white);
ctx = document.getElementById("right").getContext("2d");
height = 512;
width = 512;
draw(perlin);

function draw(grid) {
block_w = width / grid[0].length;
block_h = height / grid.length;
for (var y = 0; y < grid.length; y++) {
  for (var x = 0; x < grid[0].length; x++) {
    var val = grid[y][x];
    var color;
    if (val == 0) {
      color = "#131391";
    }
    else if (val == 1) {
      color = "#2221FF";
    }
    else if (val == 2) {
      color = "#1BBF00";
    }
    else if (val == 3) {
      color = "#127F00";
    }
    else if (val == 4) {
      color = "#094000";
    }
    else if (val == 5) {
      color = "#403B23";
    }
    ctx.fillStyle = color;
    ctx.fillRect(x * block_w, y * block_h, block_w, block_h);
  }
}
}
