const fontSizeSlider = document.getElementById('fontSizeSlider');
const fontSizeValue = document.getElementById('fontSizeValue');

/* DISPLAY DEFAULT VALUE */

fontSizeValue.innerHTML = `${fontSizeSlider.value}pt`;

/* UPDATE VALUE ON SLIDE */

fontSizeSlider.oninput = function () {
  fontSizeValue.innerHTML = `${this.value}pt`;
};
