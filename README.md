You've run into a common issue with Markdown rendering. Sometimes, the reference-style links used for badges don't display correctly depending on the viewer or a subtle syntax issue.

Using a more direct HTML-based approach for the badges is more robust and ensures they will be displayed correctly everywhere. I've updated the `README.md` to use this method for both the top shields and the "Built With" section.

Here is the corrected version:

***

<!-- Improved compatibility of back to top link -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<div align="center">
  <a href="https://github.com/dettinjo/LLM-Fact-Auditor/graphs/contributors">
    <img alt="Contributors" src="https://img.shields.io/github/contributors/dettinjo/LLM-Fact-Auditor.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/dettinjo/LLM-Fact-Auditor/network/members">
    <img alt="Forks" src="https://img.shields.io/github/forks/dettinjo/LLM-Fact-Auditor.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/dettinjo/LLM-Fact-Auditor/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/dettinjo/LLM-Fact-Auditor.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/dettinjo/LLM-Fact-Auditor/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/dettinjo/LLM-Fact-Auditor.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/dettinjo/LLM-Fact-Auditor/blob/main/LICENSE">
    <img alt="MIT License" src="https://img.shields.io/github/license/dettinjo/LLM-Fact-Auditor.svg?style=for-the-badge">
  </a>
</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">LLM Fact Auditor</h3>

  <p align="center">
    A post-processing pipeline to fact-check, entity-link, and verify answers from Large Language Models.
    <br />
    <br />
    <a href="#about-the-project">About the Project</a>
    &middot;
    <a href="#getting-started">Getting Started</a>
    &middot;
    <a href="#usage">Usage</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Large Language Models (LLMs) are powerful, but they can produce factually incorrect or unverifiable information—a phenomenon often called "hallucination." This project, **LLM Fact Auditor**, serves as a robust post-processing pipeline designed to address this challenge. It takes a question and a raw LLM-generated answer, then enriches and verifies it through a multi-stage process.

Here's what it does:
*   **Entity Linking**: It identifies named entities (like people, places, and organizations) in the text and links them to their corresponding Wikipedia pages, grounding the response in factual data.
*   **Answer Extraction**: It distills the often verbose LLM response into a concise, direct answer, such as a "yes/no" or a specific entity.
*   **Fact-Checking**: It verifies the extracted answer's correctness by cross-referencing it with structured knowledge from Wikidata and the content of the linked Wikipedia pages.

This system was developed as a university project to create a practical tool for improving the reliability of AI-generated content.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

This project leverages a powerful stack of modern NLP tools and libraries.

<p>
  <a href="https://www.python.org/">
    <img alt="Python" src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  </a>
  <a href="https://www.docker.com/">
    <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  </a>
  <a href="https://llama.meta.com/">
    <img alt="Llama" src="https://img.shields.io/badge/LLama-2396F3?style=for-the-badge&logo=meta&logoColor=white">
  </a>
  <a href="https://pytorch.org/">
    <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">
  </a>
  <a href="https://huggingface.co/docs/transformers/index">
    <img alt="Transformers" src="https://img.shields.io/badge/Transformers-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black">
  </a>
  <a href="https://spacy.io/">
    <img alt="spaCy" src="https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white">
  </a>
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Follow these steps to set up and run the project locally within the provided Docker environment.

### Prerequisites

*   **Docker**: You must have Docker installed and running.
*   **WDPS Docker Image**: The project is designed to run inside the `karmaresearch/wdps2` Docker container. Ensure you have this container running.
    ```sh
    docker ps
    ```

### Installation

1.  **Clone the Repository**:
    ```sh
    git clone https://github.com/dettinjo/LLM-Fact-Auditor.git
    cd LLM-Fact-Auditor
    ```
2.  **Copy Project Files to Docker**: From your host machine's terminal, copy the entire project directory into your running Docker container.
    ```sh
    docker cp ./ <container_id>:/home/user/submission
    ```
3.  **Access the Container and Set Up Environment**:
    ```sh
    # Enter the container's shell
    docker exec -it <container_id> bash

    # Navigate to the project directory
    cd /home/user/submission

    # Switch to root user to install dependencies
    sudo su

    # Create and activate a virtual environment
    python3 -m venv virtual_env
    source virtual_env/bin/activate
    ```
4.  **Install Dependencies**: Install all required Python packages and download the necessary NLP models. This step may take some time.
    ```sh
    # Install Python packages
    pip install -r requirements.txt

    # Run the setup script to download all models
    python src/setup.py
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

The main script is designed to read questions from standard input and write the processed output to standard output.

### Running with Llama 2 (Default)
This command reads questions from `test_data/input.txt` and saves the structured output to `test_data/output.txt`.

```sh
python3 main.py < ./test_data/input.txt > ./test_data/output.txt
```

### Running with Llama 3
For higher quality answers and faster performance, you can use the Llama 3 model by adding the `--llama_ver=3` flag.

```sh
python3 main.py --llama_ver=3 < ./test_data/input.txt > ./test_data/output.txt
```

### Example Input & Output

**Input Question in `input.txt`:**
```
question-001	Is Managua the capital of Nicaragua?
```

**Corresponding Output in `output.txt`:**```
question-001	R"Yes, Managua is the capital and largest city of Nicaragua."
question-001	A"yes"
question-001	C"correct"
question-001	E"Managua"	"https://en.wikipedia.org/wiki/Managua"
question-001	E"Nicaragua"	"https://en.wikipedia.org/wiki/Nicaragua"
```
The output format includes the raw **R**esponse, extracted **A**nswer, **C**orrectness check, and linked **E**ntities.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Implement a more robust relation extraction module.
- [ ] Add support for additional knowledge bases beyond Wikidata.
- [ ] Develop a simple web interface for interactive demonstrations.
- [ ] Expand fact-checking capabilities to handle more complex and nuanced claims.

See the [open issues](https://github.com/dettinjo/LLM-Fact-Auditor/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

This project was created for the Web Data Processing Systems course (XM_40020) at Vrije Universiteit Amsterdam.

**Group Members:**
*   Joel Dettinger - j.dettinger@student.vu.nl
*   Ruida Zhou - r.zhou4@student.vu.nl
*   Hongqian Xia - h.xia@student.vu.nl
*   Angelo De Nadai - a.denadai@student.vu.nl

Project Link: [https://github.com/dettinjo/LLM-Fact-Auditor](https://github.com/dettinjo/LLM-Fact-Auditor)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

*   Vrije Universiteit Amsterdam
*   Hugging Face for the incredible `transformers` library and model hosting.
*   The developers of spaCy, Stanza, and the Wikidata platform.
*   [Othneil Drew's Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
