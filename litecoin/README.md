Spazio riservato al progetto su Litecoin
github

La tesina contiene tutta la ricerca.
La libreria litecoin.py contiene una serie di funzioni utili per interagire col database creato da Abe attraverso l'entità balance, che va creata manualmente.
I due sorgenti year.py e month.py servono per riempire le entità year e year_month, che vanno create manualmente, utili per fare interrogazioni statistiche, con gli anni dal 2010 al 2020.
Il sorgente prices.py serve per riempire l'entità price con uno storico scaricabile da internet. Il nome del file viene dato come argomento da linea di comando e l'id della catena va aggiunto manualmente a parte.
Le due funzioni di update invece per aggiornare le entità year e year_month.
Il file myAppConfig.py va completato inserendo tra virgolette i dati di collegamento e contiene le informazioni per collegarsi al database attraverso psycopg2.
Il file abe-pg.conf va completato inserendo tra virgolette i dati di collegamento e contiene le impostazioni di configurazione per far funzionare Abe sul database.
Il file ltc_scrypt.so contiene il modulo per far funzionare Abe con la catena di Litecoin.
Questi ultimi due vanno inseriti nella cartella di Abe, scaricabile da github all'indirizzo https://github.com/bitcoin-abe/bitcoin-abe.
