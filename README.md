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

- Right now we do not have a demo website yet because the project is still in active development and I haven't decided on a VPS provider yet. Eventually we will have a working demo, and maybe later I will even think of adding accounts for you to log in to 😉

`FUTURE DEMO LINK WILL BE PASTED HERE`

- For now you have to run it locally or you would need to host this yourself 😝

### Running locally

- Clone the GitHub repo

```bash
git clone --depth 1 https://github.com/BhaswarDutta/morpheus_md.git
```

- You need to have `uv` installed for the python dependency and virtual environment management
- On your machine you would also need `pandoc` and it's rendering engine we are currently using `weasyprint` to be installed.
- On Arch Linux it's a simple command, look into your OS of choice on how to install the dependencies. (_PS. If you're on Windows use WSL for the sake of your sanity._)

```bash
sudo pacman -S uv pandoc python-weasyprint
```

- Get inside the directory of the `backend` folder

```bash
cd morpheus_md/backend
```

- Install python dependencies using `uv`

```bash
uv sync
```

- Run the server

```bash
uv run fastapi dev main.py
```

- If you need the AI features you would need your key for Gemini. Feel free to change it to your favorite AI provider, only reason I am using Gemini is because it has a nice free tier. (_AI Features are still a Work in Progress. Though I expect to be done soon._)
- Now while inside the `backend` folder create a `.env` file
- Go to [Google AI Studio](https://aistudio.google.com/) and get your free API key
- Add your API key to the `.env` file as follows

```
GOOGLE_API_KEY=your_api_key
```

- Test if your API key is working using a python script I have already made for that

```bash
uv run test_gemini_api.py
```

- If you get the following output, congrats your API is working

```
✅ CONNECTION SUCCESSFUL!
🤖 Gemini 3 says: Morpheus is online.
```

## Feature Roadmap

- [x] **v0**
  - [x] Simple bash script with resume conversion using `pandoc`, `weasyprint` and a custom `css` file
- [x] **v1**
  - [x] Web App based on `HTMX` and `FastAPI` which gives the bash script a nice UX with a monochrome CSS look
  - [x] Add a global font size option if you want to cram your resume into a single page. (_Some ATS systems need you to do it_ 😞)
- [ ] **v1.1**
  - [x] Frontend button for convert to proper formatted Markdown using AI
  - [x] Frontend button for tailor to Job Description using AI
  - [ ] Backend APIs connecting to Gemini and having predefined prompts
- [ ] **v2** (_Future Plans_)
  - [ ] Switching `pdf` conversion to using `LaTeX` over `weasyprint` and `CSS`
  - [ ] Multiple templates for different needs and different designs
  - [ ] Custom `LaTeX` support if you already have a Resume in `LaTeX`
  - [ ] Support for importing `.docx` files if you have Word Docs
- [ ] **v3** (_Further future plans maybe?_)
  - [ ] I'm not happy with the markdown typing experience in the Web App so I might integrate a JS library or write something from scratch (_Right now I personally use Obsidian to write all my markdown in._)
