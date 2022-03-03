# Chatbot Presidentielle 2022
Chatbot project @CentraleSupélec for the French presidential election of 2022 made with [rasa](https://rasa.com/)

## Installation
```bash 
source venv/bin/activate
```

```bash 
rasa run 
rasa run actions
rasa shell
```

```bash 
ngrok http 5005
```

## Usage
This project is only an experimentation for a school project and has therefore no political use. We try to make it as neutral as possible, if any issue is observed please raise an issue. 

## Roadmap

## Word2vec embedding

https://fauconnier.github.io/

Binary model used : `frWac_non_lem_no_postag_no_phrase_500_skip_cut100.bin` (bin (298Mb) : skip-gram, dim 500, cut 100)

The `.bin` file must be downloaded and placed in `data/word2vec/`.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT]()

## Project status
In development - project deadline: 13 April 22'

## References
[1] Yejin Bang and Nayeon Lee and Etsuko Ishii and Andrea Madotto and Pascale Fung, Assessing Political Prudence of Open-domain Chatbots, [arXiv preprint arXiv:2106.06157](https://arxiv.org/abs/2106.06157),2021  
[2] Miller, A.~H. and Feng, W. and Fisch, A. and Lu, J. and Batra, D. and Bordes, ParlAI: A Dialog Research Software Platform, [arXiv preprint arXiv:1705.06476](https://arxiv.org/abs/2004.13637), 2017
