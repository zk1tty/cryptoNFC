use smart_contract::log;
use smart_contract::transaction::Transfer;
use smart_contract::transaction::Transaction;
use smart_contract::payload::Parameters;
use smart_contract::crypto::SignatureAlgorithm;
use smart_contract_macros::smart_contract;

pub struct Contract {
    pub public_key: [u8; 32],
    pub owner: [u8; 32],
    pub amount: u64,
}

#[smart_contract]
impl Contract {
    fn init(params: &mut Parameters) -> Self {
        Self {
            public_key: [0; 32],
            owner: params.sender,
            amount: 0,
        }
    }

    fn set_public_key(&mut self, params: &mut Parameters) -> Result<(), String> {
        let ic: [u8; 32] = params.read();
        self.public_key = ic;

        Ok({})
    }

    fn charge_ic(&mut self, params: &mut Parameters) -> Result<(), String> {
        let amount: u64 = params.read();
        if params.sender != self.owner {
            return Err("Only the owner of this contract can charge IC".to_string());
        }

        self.amount += amount;

        log(&format!("Amount is now {}", amount));

        Ok({})
    }

    fn ic_transaction(&mut self, params: &mut Parameters) -> Result<(), String> {
        let signed_data: Vec<u8> = params.read();
        let signature: Vec<u8> = params.read();

        if let Err(_err) = smart_contract::crypto::verify(
            SignatureAlgorithm::Ed25519,
            &self.public_key, &signed_data, &signature) {
            return Err("Failed to verify signature".to_string());
        }

        let mut be_bytes: [u8; 8] = [0; 8];
        for x in 0..7 {
            be_bytes[x] = signed_data[x];
        }

        let amount = u64::from_be_bytes(be_bytes);
        if self.amount < amount {
            return Err("Not enough funds".to_string());
        }

        self.amount -= amount;

        Transfer {
            destination: params.sender,
            amount: amount,
            invocation: None,
        }
        .send_transaction();

        Ok({})
    }
}
