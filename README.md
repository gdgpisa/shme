# Smart Home Made Easy

Questo è il materiale che è stato utilizzato per il talk [Smart Home Made Easy](https://www.eventbrite.it/e/biglietti-smart-home-made-easy-51720088176).
___
##### Disclamer
Questo sorgente è stato costruito con il fine di essere semplice e comprensibile a tutti. Alcune pratiche utilizzate potrebbero essere rischiose in ambiti professionali, utilizzate il codice con cautela.
___

Potete trovare le slides utilizzate per il talk in questo [link](https://drive.google.com/file/d/1GvdwU6Fr45FLQsBTsxXKQ_W3N6T9KZlk/view?usp=sharing)
Nelle slides troverete anche le istruzioni su cosa vi serve installare nella vostra macchina per utilizzare il progetto.

#### Come lanciare il server
vi basterà andare nel terminale, collocarvi nella cartella del server ed usare il comando:
```bash
sudo python3 server.py
```

#### Importante
Per far funzionare il progetto nella vostra rete ricordate di

*  Sostituire in tutto il codice (sia server che client) il campo `my.awesome.domain` con:
    * L'ip locale del raspberry: nel caso in cui vogliate lanciare il progetto in locale
    * Il vostro dominio o l'ip pubblico: altrimenti
* Effettuare il port forwarding alla porta 80 e 443 verso il Raspberry per poter utilizzare il progetto da remoto

### Dubbi?
Per qualsiasi cosa contattaci direttamente su Telegram:
* [@gi0bart](http://t.me/gi0bart)
* [@domenicoblanco](http://t.me/domenicoblanco)





