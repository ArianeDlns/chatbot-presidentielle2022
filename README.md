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
### :whale: Build docker image

```bash
sudo docker-compose up --build
```

## Usage
This project is only an experimentation for a school project and has therefore no political use. We try to make it as neutral as possible, if any issue is observed please raise an issue. 

## Roadmap

<<<<<<< HEAD
=======
## Word2vec embedding

https://fauconnier.github.io/

Binary model used : `frWac_non_lem_no_postag_no_phrase_500_skip_cut100.bin` (bin (298Mb) : skip-gram, dim 500, cut 100)

The `.bin` file must be downloaded and placed in `data/word2vec/`.


>>>>>>> 20be8f5bb2caf0d4f8fd3287038b1e466749ea2d
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

### Deployement 
[3] https://rasa.com/docs/rasa/docker/deploying-in-docker-compose  
[4] https://www.youtube.com/watch?v=5fjL2nICnXo  
[5] https://innovationyourself.com/run-multiple-services-with-docker-compose/  
[6] https://forum.rasa.com/t/ dockerizing-my-rasa-chatbot-application-that-has-botfront/46096/27  
[7] https://rasa.com/blog/the-rasa-masterclass-handbook-episode-11/ (SSL)  
[8] https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent (SSHh keys)  
[9] https://ttt.studio/blog/rasa-chatbot/ (NGINX)  
[10] https://github.com/teniosgmbh/tenios-api-examples/tree/e4e14cbc418d2a92ab7e3562b4a09128b61717a0/RASA-PizzaBot

```bash 
sudo apt update
sudo apt install git
sudo apt install docker
sudo apt install docker-compose
git clone https://github.com/ArianeDlns/chatbot-presidentielle2022.git
git checkout deployement 
sudo docker-compose up
```

```bash
sudo nginx -s stop
sudo certbot certonly --standalone
sudo cp /etc/letsencrypt/live/projet-3a-bot-presidentielles-2022.illuin-tech.com/fullchain.pem ./certs
sudo cp /etc/letsencrypt/live/projet-3a-bot-presidentielles-2022.illuin-tech.com/privkey.pem ./certs
```
