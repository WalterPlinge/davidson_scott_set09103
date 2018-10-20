var grid;
var gridScale;
var gridSize;
var selection;

function reset() {
	grid = [
		["brook", "bbishop", "bknight", "bking", "bqueen", "bknight", "bbishop", "brook"],
		["bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn"],
		["blank", "blank", "blank", "blank", "blank", "blank", "blank", "blank"],
		["blank", "blank", "blank", "blank", "blank", "blank", "blank", "blank"],
		["blank", "blank", "blank", "blank", "blank", "blank", "blank", "blank"],
		["blank", "blank", "blank", "blank", "blank", "blank", "blank", "blank"],
		["wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn"],
		["wrook", "wbishop", "wknight", "wqueen", "wking", "wknight", "wbishop", "wrook"]
	];
	selection = [-1, -1];
}

function setup() {
	gridSize = 3 * min(windowHeight, windowWidth) / 5;
	gridScale = gridSize / 8;
	createCanvas(gridSize, gridSize);
	reset();
}

function mousePressed() {
	selection = [mouseX / size, mouseY / size];
}

function piece(x, y) {
	noFill();
	strokeWeight(3);
	if (grid[y][x].charAt(0) == 'w') {
		stroke(255);
	} else {
		stroke(0);
	}
	switch (grid[y][x]) {
		case "blank":
			break;
		case "bpawn":
		case "wpawn":
			ellipse(x * gridScale + gridScale / 2, y * gridScale + gridScale / 2, gridScale / 2, gridScale / 2);
			break;
		case "brook":
		case "wrook":
			rect(x * gridScale + gridScale / 4, y * gridScale + gridScale / 4, gridScale / 2, gridScale / 2);
			break;
		case "bbishop":
		case "wbishop":
			quad(x * gridScale + gridScale / 2, y * gridScale + gridScale / 4, x * gridScale + gridScale / 4, y * gridScale + gridScale / 2, x * gridScale + gridScale / 2, y * gridScale + 3 * gridScale / 4, x * gridScale + 3 * gridScale / 4, y * gridScale + gridScale / 2);
			break;
		case "bknight":
		case "wknight":
			triangle(x * gridScale + gridScale / 2, y * gridScale + gridScale / 4, x * gridScale + gridScale / 4, y * gridScale + 3 * gridScale / 4, x * gridScale + 3 * gridScale / 4, y * gridScale + 3 * gridScale / 4);
			break;
		case "bqueen":
		case "wqueen":
			line(x * gridScale + gridScale / 4, y * gridScale + gridScale / 4, x * gridScale + 3 * gridScale / 4, y * gridScale + 3 * gridScale / 4);
			line(x * gridScale + 3 * gridScale / 4, y * gridScale + gridScale / 4, x * gridScale + gridScale / 4, y * gridScale + 3 * gridScale / 4);
			break;
		case "bking":
		case "wking":
			line(x * gridScale + gridScale / 2, y * gridScale + gridScale / 4, x * gridScale + gridScale / 2, y * gridScale + 3 * gridScale / 4);
			line(x * gridScale + gridScale / 4, y * gridScale + gridScale / 2, x * gridScale + 3 * gridScale / 4, y * gridScale + gridScale / 2);
			break;
		default:
			break;
	}
}

function draw() {
	background(100);

	for (var x = 0; x < 8; ++x) {
		for (var y = 0; y < 8; ++y) {
			if (x % 2 == y % 2) {
				fill(200);
				strokeWeight(0);
				rect(x * gridScale, y * gridScale, gridScale, gridScale);
			}
			piece(x, y);
		}
	}
}
