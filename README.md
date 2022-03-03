# Chatbot Presidentielle 2022 

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![Open in Visual Studio Code](https://img.shields.io/badge/Editor-VSCode-blue?style=flat-square&logo=visual-studio-code&logoColor=white)](https://github.dev/ArianeDlns/chatbot-presidentielle2022/tree/main) [![GitHub issues](https://badgen.net/github/issues/ArianeDlns/chatbot-presidentielle2022)](https://GitHub.com/ArianeDlns/chatbot-presidentielle2022/issues/)

![Rasa](https://github.com/ArianeDlns/chatbot-presidentielle2022/blob/develop/img/rasa.png?raw=true)


Chatbot project @CentraleSupélec for the French presidential election of 2022 made with the framework [rasa](https://rasa.com/)

## Installation

### Word2vec embedding

[Binary model used](https://fauconnier.github.io/) : `frWac_non_lem_no_postag_no_phrase_500_skip_cut100.bin` (bin (298Mb) : skip-gram, dim 500, cut 100)

The `.bin` file must be downloaded and placed in `data/word2vec/`.

```bash
cd actions/data
mkdir word2vec
cd word2vec 
wget https://s3.us-east-2.amazonaws.com/embeddings.net/embeddings/frWac_non_lem_no_postag_no_phrase_500_skip_cut100.bin
```

### Update credentials

```bash
touch credentials.yml
vim credentials.yml 
```

Update the new `credentials.yml` following this [example](https://github.com/RasaHQ/rasa/blob/main/rasa/cli/initial_project/credentials.yml)

### :whale: Build docker image
```bash
sudo docker-compose up --build
```

## Usage
This project is only an experimentation for a school project and has therefore no political use. We try to make it as neutral as possible, if any issue is observed please raise an issue. 

### Telegram chatbot
<p align="center"> <img src="https://github.com/ArianeDlns/chatbot-presidentielle2022/blob/develop/img/exemple.png" width="100" alt="Telegram"/> 

## Roadmap

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT]()

## Project status
In development - project deadline: :calendar: 13 April 22'

## References
[1] Yejin Bang and Nayeon Lee and Etsuko Ishii and Andrea Madotto and Pascale Fung, Assessing Political Prudence of Open-domain Chatbots, [arXiv preprint arXiv:2106.06157](https://arxiv.org/abs/2106.06157),2021  
[2] Miller, A.~H. and Feng, W. and Fisch, A. and Lu, J. and Batra, D. and Bordes, ParlAI: A Dialog Research Software Platform, [arXiv preprint arXiv:1705.06476](https://arxiv.org/abs/2004.13637), 2017  

### Deployement 
[3] https://ttt.studio/blog/rasa-chatbot/ (NGINX)  


