Spazio riservato al progetto su Litecoin
github

La libreria litecoin.py contiene una serie di funzioni utili per interagire col database creato da Abe attraverso l'entità balance, che va creata manualmente.
Le due funzioni di update invece per aggiornare le entità year e year_month, che vanno create manualmente, utili per fare interrogazioni statistiche.
Il file myAppConfig.py va completato inserendo tra virgolette i dati di collegamento e contiene le informazioni per collegarsi al database attraverso psycopg2.
Il file abe-pg.conf va completato inserendo tra virgolette i dati di collegamento e contiene le impostazioni di configurazione per far funzionare Abe sul database.
Il file ltc_scrypt.so contiene il modulo per far funzionare Abe con la catena di Litecoin.
Questi ultimi due vanno inseriti nella cartella di Abe, scaricabile da github all'indirizzo https://github.com/bitcoin-abe/bitcoin-abe.
