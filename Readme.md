[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
![Coverage](test/coverage.svg)

# LooksPhishy

_Presented at [BlackHat USA 2024 Arsenal](https://www.blackhat.com/us-24/arsenal/schedule/index.html#genai-vs-phishing-39167)_

# Table of Contents

1. [Download and Getting Started](#download-and-getting-started)
2. [Brand Store](#brand-store)
3. [Model Architecture](#model-architecture)
4. [Support and Contributing to LooksPhishy](#support-and-contributing-to-looksphishy)

# Download and Getting Started

First of all, clone the repo :)

## The Quick Way - Docker

The quicker way, as (almost) always, is to run a Docker.

You can use the one I uploaded to Docker Hub to quickly start:

```shell
docker run -it -p 8080:8080 --name looksphishy guardio/looksphishy_image
```

You can also build your own Docker image by running (or if the above image is not accessible):

```shell
docker-compose up
```

Now browse to http://localhost:8080, and you should have the server up.

Moreover, this Docker image can be easily deployed to a cloud service, App Service (Azure), or Elastic Beanstalk (AWS). Enjoy :)

## The Less Quick Way - Git Clone

To run the UI, just:

```shell
streamlit run app.py
```

For the CLI, you can run the following command:

```shell
python app.py
```

On Mac, Chromedriver can be installed with:

```shell
brew install chromedriver
```

# Brand Store

LooksPhishy is brand-oriented. If you want to block any phishing imitating Facebook, for example, you need to do two things:

1. Add some screenshots of the login pages/landing pages of Facebook in the folder `static/brands/Facebook`.
2. Compute the embedding of those images with the script `src/prepare_embedding.py`.

That's it! You can now block any phishing imitating Facebook. Repeat step 1 for any brand and then just run step 2 once.

# Model Architecture

There are three kinds of models.

## Embedding - The Main Model Used to Detect Phishing

They are stored under `src/models/embedding`. Some are open-source, and some require a paid subscription. The goal of the model is to take an image and convert it into a vector (embedding). This vector is then compared with the brand store to see if it resembles one of the images.

You can add your own model by following these steps:
1. Inherit from `src/models/embedding/embedding.py`.
2. Give your model a name in the class with the `name` attribute.
3. Add it into `src/models/embedding/__init__.py` following the format of the other models.

*This automatically creates a new model in the UI as well!*

## LLM - Large Language Model

These models are used to get the category of the phishing website. They are stored under `src/models/llm`.

You can follow the same steps as for the embedding model to add your own model (just adapt it to the `llm` folder).

### Llama3 LLM Bootstrap

To get started with Llama3 LLM, follow these steps:
1. Visit the Ollama GitHub repository.
2. Download the Ollama package.
3. Run the following command to download Llama3: `ollama run llama3`.

## Logo Detection

Sometimes, getting the different logos of the website can be useful. They are stored under `src/models/logo_detection`.

You can follow the same steps as for the embedding model to add your own model (just adapt it to the `logo_detection` folder).

# Support and Contributing to LooksPhishy

This code is maintained. You are welcome to ask any questions directly on GitHub. We will try to answer as quickly as possible.

We also invite you to contribute to this open source project. Add your models, improve the UI, or fix bugs. It can be done via a pull request. More details on how to create a pull request [here](https://www.dataschool.io/how-to-contribute-on-github/). Please provide basic tests with your code.

## Running the Tests

Adding tests protects your code but also explains them to others. Make sure the project has at least 70% coverage. To check the coverage, pip install these two packages:

```bash
pip install coverage
pip install coverage-badge
```

and run from the main directory:

```bash
coverage run -m pytest
coverage report -m --omit="*/test*"  # optional - to see the coverage without including tests
coverage-badge -o test/coverage.svg -f  # this will create the coverage badge loaded in the README
```

# Authors

**Author**: [Jordan Garzon] and [Omer Yanovich]

from [Guardio](https://guard.io/)

[Jordan Garzon]: https://www.linkedin.com/in/jordan-garzon/

[Omer Yanovich]: https://www.linkedin.com/in/omer-yanovich-954a61185/

```text
                                               ____________
                                --)-----------|____________|
                                              ,'       ,'
                -)------========            ,'  ____ ,'
                         `.    `.         ,'  ,'__ ,'
                           `.    `.     ,'       ,'
                             `.    `._,'_______,'__
                               [._ _| ^--      || |
                       ____,...-----|__________ll_|\
      ,.,..-------"""""     "----'                 ||
  .-""  |=========================== ______________ |
   "-...l_______________________    |  |'      || |_]
                                [`-.|__________ll_|      Enjoy
                              ,'    ,' `.        `.      
                            ,'    ,'     `.    ____`.    
                -)---------========        `.  `.____`.
                                             `.        `.
                                               `.________`.
                               --)-------------|___________|
```