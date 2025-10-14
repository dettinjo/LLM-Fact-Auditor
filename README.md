# XM_40020_WedDataProcessingSystems
![Licence](https://img.shields.io/badge/Licence-MIT-green?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/Angelo-De-Nadai/XM_40020_WedDataProcessingSystems?style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/Angelo-De-Nadai/XM_40020_WedDataProcessingSystems?style=for-the-badge)

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#group-members">Group Members</a>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#structure">Structure</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
  </ol>
</details>

<!-- GROUP MEMBERS -->
## Group Members
- Joel Dettinger - 2837238 - j.dettinger@student.vu.nl
- Ruida Zhou - 2838822 - r.zhou4@student.vu.nl
- Hongqian Xia - 2844892 - h.xia@student.vu.nl
- Angelo De Nadai - 2866832 - a.denadai@student.vu.nl

<!-- PROJECT OVERVIEW -->
## About the Project
### Built With

- [![PythonBadge]](https://www.python.org/doc/)
- [![DockerBadge]](https://docs.docker.com/)
- [![BashBadge]](https://www.gnu.org/software/bash/manual/bash.html)
- [![MetaBadge]](https://www.llama.com/)

## Demo
### Example Question
```
question-001	Is Managua the capital of Nicaragua?
```
Output from llama 2
```
question-001	R"Yes, Managua is the capital and largest city of Nicaragua."
question-001	A"yes"
question-001	C"correct"
question-001	E"Managua"	"https://en.wikipedia.org/wiki/Managua"
question-001	E"Nicaragua"	"https://en.wikipedia.org/wiki/Nicaragua"
```


<!-- PROJECT SETUP -->

## Getting Started

### Initialization

Copy files to Docker container
```
# at submission folder, host machine
# get your container ID
user@host_machine XM_40020_WedDataProcessingSystems % docker ps

# copy files from the host into the Docker container
user@host_machine XM_40020_WedDataProcessingSystems % docker cp ./ <container_id>:/home/user/submission
```


Check if files exit in docker
```
# back to docker
user@ace396552e14:~$ cd submission/

user@ace396552e14:~/submission$ pwd
/home/user/submission

# we should have directory structure like this
user@ace396552e14:~/submission$ ls
Dockerfile  README.md  main.py     requirements.txt  test_data
LICENSE     debug.py   output.txt  src
```
Set up a virtual environment
```
# switch to root user
user@ace396552e14:~/submission$ sudo su

# set up venv
root@ace396552e14:/home/user/submission# python3 -m venv virtual_env

root@ace396552e14:~/submission$ source virtual_env/bin/activate

(virtual_env) root@ace396552e14:~/submission$ pip install -r requirements.txt

(virtual_env) root@ace396552e14:/home/user/submission# python src/setup.py
```
### Execution
### With Llama2
You can execute task 1 with the following command. The default input is `./test_data/input.txt`, which contains the question list. The result will be output to `./test_data/output.txt`, which contains RACEs. If you execute it multiple times, the result files will be overwritten.

Change input and output file path for other question sets if needed.

For the sample questions in `./test_data/input.txt`, it takes about 3 mins with llama2
```
(virtual_env) root@ace396552e14:/home/user/submission# python3 main.py < ./test_data/input.txt > ./test_data/output.txt
```
#### With Llama3

The given model llama 2 produces answers of poor quality. Add `llama_ver` param to switch to llama 3 for better answers and faster speed (less than 3 min for sample questions in `./test_data/input.txt`).
```
(virtual_env) root@ace396552e14:/home/user/submission# python3 main.py --llama_ver=3 < ./test_data/input.txt > ./test_data/output.txt
```

<!-- MARKDOWN LINKS & IMAGES -->
[PythonBadge]:https://img.shields.io/badge/python-yellow?style=for-the-badge&logo=python&logoColor=white
[DockerBadge]:https://img.shields.io/badge/Docker-%231D63ED?style=for-the-badge&logo=docker&logoColor=white
[BashBadge]:https://img.shields.io/badge/GNU%20Bash-black?style=for-the-badge&logo=gnubash&logoColor=white
[MetaBadge]:https://img.shields.io/badge/LLama-%230081FB?style=for-the-badge&logo=meta&logoColor=white
