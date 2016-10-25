var input = document.querySelector('#input');
var output = document.querySelector('#output');

input.addEventListener('keydown', function() {
	setTimeout(function() {
		output.textContent = memms(input.value);
	}, 0)
})
