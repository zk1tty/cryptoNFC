use smart_contract::log;
use smart_contract::transaction::Transfer;
use smart_contract::transaction::Transaction;
use smart_contract::payload::Parameters;
use smart_contract_macros::smart_contract;

pub struct Contract {
    pub owner: [u8; 32],
    pub amount: u64,
}

#[smart_contract]
impl Contract {
    fn init(params: &mut Parameters) -> Self {
        Self {
            owner: params.sender,
            amount: 0,
        }
    }

    fn charge_ic(&mut self, params: &mut Parameters) -> Result<(), String> {
        let amount: u64 = params.amount;

        if amount == 0 {
            return Err("Must send a PERL value along with this request".to_string());
        }

        self.amount += amount;

        log(&format!("Amount is now {}", amount));

        Ok({})
    }

    fn ic_transaction(&mut self, params: &mut Parameters) -> Result<(), String> {
        let recipient: [u8; 32] = params.read();
        let amount: u64 = params.read();

        if params.sender != self.owner {
            return Err("Only the owner of this contract can transact".to_string());
        }

        if self.amount < amount {
            return Err("Not enough funds".to_string());
        }

        self.amount -= amount;

        Transfer {
            destination: recipient,
            amount: amount,
            invocation: None,
        }
        .send_transaction();

        Ok({})
    }
}
