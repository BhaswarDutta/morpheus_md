const resumeInput = document.getElementById('resumeInput');
const resumeTextDisplay = document.getElementById('resumeTextDisplay');

let usingBoilerplate = true;

/* LOAD BOILERPLATE MARKDOWN */

fetch('/template/boilerplate_resume.md')
  .then((response) => response.text())
  .then((text) => {
    resumeTextDisplay.value = text;
    resumeTextDisplay.classList.add('placeholder-mode');
  });

/* REMOVE MUTED STYLE ON FIRST EDIT */

resumeTextDisplay.addEventListener(
  'input',
  () => {
    if (usingBoilerplate) {
      resumeTextDisplay.classList.remove('placeholder-mode');
      usingBoilerplate = false;
    }
  },
  { once: true },
);

/* UPLOAD FILE OVERRIDES BOILERPLATE */

resumeInput.addEventListener('change', () => {
  const file = resumeInput.files[0];

  if (!file) return;

  const reader = new FileReader();

  reader.onload = (event) => {
    resumeTextDisplay.value = event.target.result;

    resumeTextDisplay.classList.remove('placeholder-mode');

    usingBoilerplate = false;
  };

  reader.readAsText(file);
});
