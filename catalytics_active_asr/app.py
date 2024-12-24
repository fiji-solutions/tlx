import json


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "proposal": [
                {
                    "proposalId": "CqMsFvvmzETwwa2tXMZ75aNvjc5xy7VamxYC5u7v1ScA",
                    "proposalName": "Which animal is the cutest?",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Cats"
                        },
                        {
                            "side": 2,
                            "name": "Raccoons"
                        },
                        {
                            "side": 3,
                            "name": "Lions"
                        },
                        {
                            "side": 4,
                            "name": "Tigers"
                        },
                    ]
                },
                {
                    "proposalId": "6txWyf3guJrhnNJXcAHxnV2oVxBcvebuSbfYsgB3yUKc",
                    "proposalName": "Round #1 of LFG Voting!",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Sharky"
                        },
                        {
                            "side": 2,
                            "name": "UpRock"
                        },
                        {
                            "side": 3,
                            "name": "Banx"
                        },
                        {
                            "side": 4,
                            "name": "Zeus Network"
                        },
                        {
                            "side": 5,
                            "name": "Monkey Dex"
                        },
                        {
                            "side": 6,
                            "name": "Srcful"
                        },
                    ]
                },
                {
                    "proposalId": "5N9UbMGzga3SL8Rq7qDZCGfZX3FRDUhgqkSY2ksQjg8r",
                    "proposalName": "Proposal: Core Working Group Budget",
                    "proposalChoices": [
                        {
                            "side": 0,
                            "name": "Abstain"
                        },
                        {
                            "side": 1,
                            "name": "Against"
                        },
                        {
                            "side": 2,
                            "name": "For"
                        }
                    ]
                },
                {
                    "proposalId": "2c2Yg1E9BNQVxqg9ZpB2CTBa4GGT8CoeWH6JN7ZQ5FDw",
                    "proposalName": "Round #2 of LFG Voting",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Sanctum"
                        },
                        {
                            "side": 2,
                            "name": "UpRock"
                        },
                        {
                            "side": 3,
                            "name": "Srcful"
                        },
                        {
                            "side": 4,
                            "name": "MonkeyDex"
                        },
                        {
                            "side": 5,
                            "name": "Nyan Heroes"
                        },
                        {
                            "side": 6,
                            "name": "Solana ID"
                        },
                    ]
                },
                {
                    "proposalId": "A37zp1811aYLd7uoXN78KG12csC9dycyJcK7dD3R22zo",
                    "proposalName": "Trial Budget: Web Working Group",
                    "proposalChoices": [
                        {
                            "side": 0,
                            "name": "Abstain"
                        },
                        {
                            "side": 1,
                            "name": "Against"
                        },
                        {
                            "side": 2,
                            "name": "For"
                        },
                    ]
                },
                {
                    "proposalId": "DhJAwGDtHYdEy8mBoeZ3Yub5potxRJbvzycYUwhFGfox",
                    "proposalName": "Trial Budget: Catdet Working Group",
                    "proposalChoices": [
                        {
                            "side": 0,
                            "name": "Abstain"
                        },
                        {
                            "side": 1,
                            "name": "Against"
                        },
                        {
                            "side": 2,
                            "name": "For"
                        },
                    ]
                },
                {
                    "proposalId": "5QTT1AFSMA76dNUFYETiEAo54q3vKvGc8WexTGjamHDN",
                    "proposalName": "Trial Budget: Reddit Working Group",
                    "proposalChoices": [
                        {
                            "side": 0,
                            "name": "Abstain"
                        },
                        {
                            "side": 1,
                            "name": "Against"
                        },
                        {
                            "side": 2,
                            "name": "For"
                        },
                    ]
                },
                {
                    "proposalId": "GiPupbvjySF8XQr7NPk8z3HhLkkreuZ7pdDqcyaSWMXN",
                    "proposalName": "Round #3 of LFG Voting",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "deBridge"
                        },
                        {
                            "side": 2,
                            "name": "ExchangeArt"
                        },
                        {
                            "side": 3,
                            "name": "Divvy.Bet"
                        },
                    ]
                },
                {
                    "proposalId": "CioyJmzFuRbN3Pda1LhvNxsEDoA4gQfTJ56F2hgWib5C",
                    "proposalName": "Proposal: Uplink Working Group Budget",
                    "proposalChoices": [
                        {
                            "side": 0,
                            "name": "Abstain"
                        },
                        {
                            "side": 1,
                            "name": "Against"
                        },
                        {
                            "side": 2,
                            "name": "For"
                        },
                    ]
                },
                {
                    "proposalId": "CnzPx1KQu1SFvGJHpZ4ykNkmfHSLBKx1oVESyjb5CjYC",
                    "proposalName": "J4J #1: Supply Reduction Proposal",
                    "proposalChoices": [
                        {
                            "side": 0,
                            "name": "Abstain"
                        },
                        {
                            "side": 1,
                            "name": "Against"
                        },
                        {
                            "side": 2,
                            "name": "For"
                        },
                    ]
                },
                {
                    "proposalId": "CudfcXyY6JWKFkZxHMLv9ZvJuzBat4UvTx6anzW33TvM",
                    "proposalName": "Jupiter DAO: Microgrants Proposal",
                    "proposalChoices": [
                        {
                            "side": 0,
                            "name": "Abstain"
                        },
                        {
                            "side": 1,
                            "name": "Against"
                        },
                        {
                            "side": 2,
                            "name": "For"
                        },
                    ]
                },
                {
                    "proposalId": "ApKpFDzwsjMEpW4zPNpmsHyPGfKrjaY6rA9HTLwV5a1w",
                    "proposalName": "Trial Budget: Jup & Juice WG (JJWG)",
                    "proposalChoices": [
                        {
                            "side": 0,
                            "name": "Abstain"
                        },
                        {
                            "side": 1,
                            "name": "Against"
                        },
                        {
                            "side": 2,
                            "name": "For"
                        },
                    ]
                },
                {
                    "proposalId": "5G3ut22wiUWAoSnHCNTHus8LJTcnUaJKzjH1j1vLvoKs",
                    "proposalName": "J4J #2: Utilize Excess Jupuary for ASR",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Fund ASR for 1 year"
                        },
                        {
                            "side": 2,
                            "name": "Burn the tokens"
                        },
                        {
                            "side": 3,
                            "name": "Return to Community Multisig"
                        },
                    ]
                },
                {
                    "proposalId": "PJVgLKqBa5LabApp9uU5rvxUgqp4RdUfBxVbEddLxWa",
                    "proposalName": "Proposal: Increase Quorum for Jupiter DAO",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Leave at 60M JUP"
                        },
                        {
                            "side": 2,
                            "name": "Increase to 120M JUP"
                        },
                        {
                            "side": 3,
                            "name": "Peg to 30% of Staked JUP"
                        },
                    ]
                },
                {
                    "proposalId": "ByQ21v3hqdQVwPHsfwurrtEAH8pB3DYuLdp9jU2Hwnd4",
                    "proposalName": "JUP Mobile Background Vote",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Burning Cat"
                        },
                        {
                            "side": 2,
                            "name": "PPP"
                        },
                        {
                            "side": 3,
                            "name": "In Space"
                        },
                        {
                            "side": 4,
                            "name": "Discovery"
                        },
                        {
                            "side": 5,
                            "name": "Jupiverse??"
                        },
                        {
                            "side": 6,
                            "name": "The Current Default"
                        },
                    ]
                },
                {
                    "proposalId": "CWAwYcLmniqQYnzDh3QGRH6FtymBesJ9dzk1EBvYNBwK",
                    "proposalName": "J4J #3: Jupuary Vote 1",
                    "startDate": "2024-11-25T16:00:00.000000",
                    "endDate": "2024-11-29T16:00:00.000000",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Yes, I am comfortable with this proposal.",
                            "title": "Yes"
                        },
                        {
                            "side": 2,
                            "name": "No, I am not comfortable with this proposal.",
                            "title": "No"
                        },
                    ]
                },
                {
                    "proposalId": "xMLsw7zzBfRXNiQQo42aUohRsibgrmWcPt2mD8HdUUr",
                    "proposalName": "J4J #3: Jupuary Vote 2",
                    "startDate": "2024-12-04T04:00:00.000000",
                    "endDate": "2024-12-08T04:00:00.000000",
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Yes, I am comfortable with this proposal.",
                            "title": "Yes"
                        },
                        {
                            "side": 2,
                            "name": "No, I am not comfortable with this proposal.",
                            "title": "No"
                        },
                    ]
                },
            ],
            "activeProposal": [],
        }),
    }
