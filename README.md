# Morpheus Resume MD

_Tailor your resume for each Job Application in two clicks_

- Have a default resume, but manually changing it for Job Applications for each company you apply to can be tedious 🤯
- Especially in an era where companies use ATS systems to auto reject resumes without the needed keywords 😭
- This system has many flaws but unfortunately this is what the industry standard
- So you need to apply in bulk to even get a response, but you also want to tailor your resume for each Job Description to make sure your Resume has the right keywords?
- Do not worry, if companies can use AI to filter through your resume then we have the power of AI too, to inject keywords in bulk 💪
- To achieve this we use the power of Markdown files 📄

## What is Markdown?

- Markdown files are a simple way to have a file which has headings and stuff like that without depending on some word doc.
- This description you are reading is the `README.md` markdown file for this project
- And Markdown is also used by your favorite LLMs to output their text be it ChatGPT, Claude, Gemini, Deepseek or Qwen.
- Thus we convert our resume into Markdown format to have a base and then use LLMs with the JD to inject needed keywords without changing the actual contents

## But companies need a `.pdf` file!

- Yeah you are right, and we have solved it too using the amazing power of CSS and an amazing tool called `pandoc`
- `pandoc` is primarily a Command Line Tool but here we have streamlined it into a Web App which automatically styles your PDF.
- Right now we have only one style but later in the project we would be working on improving that

## Getting Started

### Demo Website

- This is what I have hosted on my VPS at: [morpheus-md.cloud](https://morpheus-md.cloud/)
- I still have accounts to be implemented so if you need something with a large number of API requests host it yourself
- Later I will introduce a paid tier because I am a capitalist 😼
- No seriously I literally have my free tier of Gemini API out in the open and if the website views are large I would move on to a paid tier of Gemini API which is faster but also costs me money. Thus I will have to charge for it for this Website to be sustainable.
- But hey if you do now want to pay for it you can always run it locally on your machine with your own Free Gemini Key.

### Running locally

- I moved this section to a separate Wiki section in GitHub.
- Check it out at [Morpheus MD Wiki](https://github.com/BhaswarDutta/morpheus_md/wiki)
-

## Feature Roadmap

- [x] **v0**
  - [x] Simple bash script with resume conversion using `pandoc`, `weasyprint` and a custom `css` file
- [x] **v1**
  - [x] Web App based on `HTMX` and `FastAPI` which gives the bash script a nice UX with a monochrome CSS look
  - [x] Add a global font size option if you want to cram your resume into a single page. (_Some ATS systems need you to do it_ 😞)
- [x] **v1.1**
  - [x] Frontend button for convert to proper formatted Markdown using AI
  - [x] Frontend button for tailor to Job Description using AI
  - [x] Backend APIs connecting to Gemini and having predefined prompts
  - [x] Dockerize the project for easier deployment
  - [x] Demo deployed at [morpheus-md.cloud](https://morpheus-md.cloud/)
- [ ] **v2** (_Future Plans_)
  - [ ] UX improvements
    - [ ] Better popups when Gemini is down
  - [ ] Switching `pdf` conversion to using `LaTeX` over `weasyprint` and `CSS`
  - [ ] Multiple templates for different needs and different designs
  - [ ] Custom `LaTeX` support if you already have a Resume in `LaTeX`
  - [ ] Support for importing `.docx` files if you have Word Docs
  - [ ] I'm not happy with my project being entirely reliant of Google's Gemini. I want it to be able to work with multiple LLM providers and eventually a self hosted one.
    - [ ] Integration with other LLM APIs such as OpenAI and Anthropic
    - [ ] Integration with locally running LLMs such as Deepseek or Qwen
- [ ] **v3** (_Further future plans maybe?_)
  - [ ] I'm not happy with the markdown typing experience in the Web App so I might integrate a JS library or write something from scratch (_Right now I personally use Obsidian to write all my markdown in._)

---

<p align="center">
  Made with ❤️ for Open Source Software.
</p>

<p align="center">
  This project is MIT licensed, so use it however you want.
</p>

<p align="center">
  If you build something cool with it, do tag me on Twitter 😉
</p>
