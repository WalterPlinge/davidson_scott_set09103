var grid = [];
var player = 'x';
var width;
var height;

function swapPlayer() {
	switch (player) {
		case 'x':
			player = 'o';
			break;
		case 'o':
			player = 'x';
			break;
		default:
			break;
	}
}

function reset() {
	for (var i = 0; i < 9; ++i) {
		grid[i] = ' ';
	}
	player = 'o';
}

function setup() {
	height = width = 3 * min(windowHeight, windowWidth) / 5;
	createCanvas(width, height);
	reset();
}

function mousePressed() {
	var play = 0;
	if (mouseY > height || mouseY < 0 || mouseX > width || mouseX < 0) {
		play = -1;
	}
	if (mouseY < height / 3) {
		if (mouseX < width / 3) {
			play = 0;
		} else if (mouseX > 2 * width / 3) {
			play = 2;
		} else {
			play = 1;
		}
	} else if (mouseY > 2 * height / 3) {
		if (mouseX < width / 3) {
			play = 6;
		} else if (mouseX > 2 * width / 3) {
			play = 8;
		} else {
			play = 7;
		}
	} else {
		if (mouseX < width / 3) {
			play = 3;
		} else if (mouseX > 2 * width / 3) {
			play = 5;
		} else {
			play = 4;
		}
	}
	if (play != -1 && grid[play] == ' ') {
		grid[play] = player;
		swapPlayer();
	}
}

function drawCircle(x, y) {
	ellipse(x * width / 3 + width / 6, y * height / 3 + height / 6, width / 7, height / 7);
}

function drawCross(x, y) {
	line(x * width / 3 + width / 9, y * height / 3 + height / 9, x * width / 3 + 2 * width / 9, y * height / 3 + 2 * height / 9);
	line(x * width / 3 + width / 9, y * height / 3 + 2 * height / 9, x * width / 3 + 2 * width / 9, y * height / 3 + height / 9);
}

function drawGrid() {
	line(0, height / 3, width, height / 3);
	line(0, 2 * height / 3, width, 2 * height / 3);
	line(width / 3, 0, width / 3, height);
	line(2 * width / 3, 0, 2 * width / 3, height);
}

function draw() {
	background(255);

	drawGrid();

	for (var x = 0; x < 3; ++x) {
		for (var y = 0; y < 3; ++y) {
			switch (grid[y * 3 + x]) {
				case 'o':
					drawCircle(x, y);
					break;
				case 'x':
					drawCross(x, y);
					break;
				default:
					break;
			}
		}
	}
}
