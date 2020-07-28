# Block

def createBlockTable():
    return "CREATE TABLE Block (hash VARCHAR(64) NOT NULL, magic_number VARCHAR(64) NOT NULL, block_size INTEGER NOT NULL, version INTEGER NOT NULL, previous_hash VARCHAR(64) NOT NULL, merkle_root VARCHAR(64) NOT NULL, time TIMESTAMP NOT NULL, bits BIGINT NOT NULL, nonce BIGINT NOT NULL, count_of_transaction INTEGER NOT NULL, CONSTRAINT PK_Block PRIMARY KEY (hash));"

def dropBlockTable():
    return "ALTER TABLE Block DROP CONSTRAINT PK_Block;DROP TABLE Block;"

def insertBlockINTO():
    return "INSERT INTO Block (hash, magic_number, block_size, version, previous_hash, merkle_root, time, bits, nonce, count_of_transaction) VALUES"

# Transaction

def createTransactionTable():
    return "CREATE TABLE Transaction (hash VARCHAR(64) NOT NULL, hash_block VARCHAR(64) NOT NULL, locktime INTEGER NOT NULL, input_count INTEGER NOT NULL, output_count INTEGER NOT NULL, version INTEGER NOT NULL, CONSTRAINT FK_Block FOREIGN KEY (hash_block) REFERENCES Block(hash), CONSTRAINT PK_Transaction PRIMARY KEY (hash));"

def dropTransactionTable():
    return "ALTER TABLE Transaction DROP CONSTRAINT Fk_Block;ALTER TABLE Transaction DROP CONSTRAINT Pk_Transaction;DROP TABLE Transaction;"

def insertTransactionINTO():
    return "INSERT INTO Transaction(hash, hash_block, locktime, input_count, output_count, version) VALUES"

# Address

def createAddressTable():
    return "CREATE TABLE Address (name VARCHAR(35) NOT NULL, CONSTRAINT Pk_Address PRIMARY KEY(name));"

def dropAddressTable():
    return "ALTER TABLE Address DROP CONSTRAINT Pk_Address;DROP TABLE Address;"

def insertAddressINTO():
    return "INSERT INTO Address(name) VALUES"

# Input

def createInputTable():
    return "CREATE TABLE Input (address VARCHAR(35) NOT NULL, hash_transaction VARCHAR(64) NOT NULL, inputIndex BIGINT NOT NULL, previous_hash VARCHAR(64) NOT NULL, out_id BIGINT, script_length BIGINT, script_signature VARCHAR(300), seqNo VARCHAR(8), CONSTRAINT Fk_Address FOREIGN KEY(address) REFERENCES Address(name), CONSTRAINT Fk_Transaction FOREIGN KEY(hash_transaction) REFERENCES Transaction(hash), CONSTRAINT Pk_Input PRIMARY KEY(address, hash_transaction, inputIndex));"

def dropInputTable():
    return "ALTER TABLE Input DROP CONSTRAINT Fk_Address;ALTER TABLE Input DROP CONSTRAINT Fk_Transaction;DROP TABLE Input;"

def insertInputINTO():
    return "INSERT INTO Input(address, hash_transaction, inputIndex, previous_hash, out_id, script_length, script_signature, seqNo) VALUES"

# Output

def createOutputTable():
    return "CREATE TABLE Output (address VARCHAR(35) NOT NULL, hash_transaction VARCHAR(64) NOT NULL, outputIndex BIGINT NOT NULL, value FLOAT NOT NULL, script_length BIGINT, script_signature VARCHAR(300), CONSTRAINT Fk_Address FOREIGN KEY(address) REFERENCES Address(name), CONSTRAINT Fk_Transaction FOREIGN KEY(hash_transaction) REFERENCES Transaction(hash), CONSTRAINT Pk_Output PRIMARY KEY(address, hash_transaction, outputIndex));"

def dropOutputTable():
    return "ALTER TABLE Output DROP CONSTRAINT Fk_Address;ALTER TABLE Output DROP CONSTRAINT Fk_Transaction;DROP TABLE Output;"

def insertOutputINTO():
    return "INSERT INTO Output(address, hash_transaction, outputIndex, value, script_length, script_signature) VALUES"

# Quotation

def createQuotationTable():
    return "CREATE TABLE Quotation (source VARCHAR(50) NOT NULL, start_date TIMESTAMP NOT NULL, end_date TIMESTAMP NOT NULL, price FLOAT NOT NULL, CONSTRAINT Pk_Quotation PRIMARY KEY(source, start_date))"

def dropQuotationTable():
    return "ALTER TABLE Quotation DROP CONSTRAINT Pk_Quotation;DROP TABLE Quotation;"

def insertQuotationINTO():
    return "INSERT INTO Quotation(source, start_date, end_date, price) VALUES"