# Differential Prompting

## Demo

<iframe width="1120" height="630" src="https://www.youtube.com/embed/BKdGuEy--UQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Description

Differential Prompting is an approach that can effectively find failure-inducing test cases with the help of the compliable code synthesized by the inferred intention. This command line tool allows users to interact with ChatGPT to automatically generate intention, code, and test input pools.

## Installation

1. Clone or download our code to your local machine:

   ```bash
   git clone https://github.com/differential-prompting/differential-prompting
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the command line tool, run the following command:

```bash
python -m diffPrompt [OPTIONS] COMMAND [ARGS]...
```

The available options and commands are:

```
Usage: python -m diffPrompt [OPTIONS] COMMAND [ARGS]...

Options:
  --version         Show the version and exit.
  --model TEXT      The OpenAI model type.
  --code_path TEXT  The code path which need to be tested.
  --proxy TEXT      Weather use proxy.
  --help            Show this message and exit.

Commands:
  update  Update the OpenAI API key.
```

#### Example

Update an OpenAI API key:

```bash
python -m diffPrompt update
```

Generate intention, codes and test inputs pool for given code.

```bash
 python -m diffPrompt --code_path example\example_code.py --proxy True 
 
 ---
 Generate intention
 Waiting for chatgpt...
 ....
 ....
 ....
 Done and save the results in :Results/example_code.py_dbd51d 
```

Once the command is executed, the results will be saved in the `Results` directory.

Overall, this optimized instruction should be easier for users to understand and follow.
