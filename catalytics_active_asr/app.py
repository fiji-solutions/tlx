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
                    "asrId": "1",
                    "proposalId": "CqMsFvvmzETwwa2tXMZ75aNvjc5xy7VamxYC5u7v1ScA",
                    "proposalName": "Which animal is the cutest?",
                    "startDate": "2024-03-05T15:50:00.000000",
                    "endDate": "2024-03-07T15:50:00.000000",
                    "totalVotes": 140857857,
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
                    "asrId": "1",
                    "proposalId": "6txWyf3guJrhnNJXcAHxnV2oVxBcvebuSbfYsgB3yUKc",
                    "proposalName": "Round #1 of LFG Voting!",
                    "startDate": "2024-03-07T16:00:00.000000",
                    "endDate": "2024-03-10T16:00:00.000000",
                    "totalVotes": 201857511,
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
                    "asrId": "1",
                    "proposalId": "5N9UbMGzga3SL8Rq7qDZCGfZX3FRDUhgqkSY2ksQjg8r",
                    "proposalName": "Proposal: Core Working Group Budget",
                    "startDate": "2024-03-29T16:03:00.000000",
                    "endDate": "2024-04-01T17:03:00.000000",
                    "totalVotes": 198987007,
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
                    "asrId": "1",
                    "proposalId": "2c2Yg1E9BNQVxqg9ZpB2CTBa4GGT8CoeWH6JN7ZQ5FDw",
                    "proposalName": "Round #2 of LFG Voting",
                    "startDate": "2024-04-17T18:00:00.000000",
                    "endDate": "2024-04-20T18:00:00.000000",
                    "totalVotes": 230849743,
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
                    "asrId": "1",
                    "proposalId": "A37zp1811aYLd7uoXN78KG12csC9dycyJcK7dD3R22zo",
                    "proposalName": "Trial Budget: Web Working Group",
                    "startDate": "2024-05-02T16:00:00.000000",
                    "endDate": "2024-05-05T16:00:00.000000",
                    "totalVotes": 189310211,
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
                    "asrId": "1",
                    "proposalId": "DhJAwGDtHYdEy8mBoeZ3Yub5potxRJbvzycYUwhFGfox",
                    "proposalName": "Trial Budget: Catdet Working Group",
                    "startDate": "2024-05-02T16:00:00.000000",
                    "endDate": "2024-05-05T16:00:00.000000",
                    "totalVotes": 188577101,
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
                    "asrId": "1",
                    "proposalId": "5QTT1AFSMA76dNUFYETiEAo54q3vKvGc8WexTGjamHDN",
                    "proposalName": "Trial Budget: Reddit Working Group",
                    "startDate": "2024-05-02T16:01:00.000000",
                    "endDate": "2024-05-05T16:01:00.000000",
                    "totalVotes": 189406552,
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
                    "asrId": "1",
                    "proposalId": "GiPupbvjySF8XQr7NPk8z3HhLkkreuZ7pdDqcyaSWMXN",
                    "proposalName": "Round #3 of LFG Voting",
                    "startDate": "2024-05-22T18:03:00.000000",
                    "endDate": "2024-05-25T18:03:00.000000",
                    "totalVotes": 217498626,
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
                    "asrId": "1",
                    "proposalId": "CioyJmzFuRbN3Pda1LhvNxsEDoA4gQfTJ56F2hgWib5C",
                    "proposalName": "Proposal: Uplink Working Group Budget",
                    "startDate": "2024-06-16T16:31:00.000000",
                    "endDate": "2024-06-19T16:31:00.000000",
                    "totalVotes": 177958478,
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
                    "asrId": "2",
                    "proposalId": "CnzPx1KQu1SFvGJHpZ4ykNkmfHSLBKx1oVESyjb5CjYC",
                    "proposalName": "J4J #1: Supply Reduction Proposal",
                    "startDate": "2024-08-01T16:16:00.000000",
                    "endDate": "2024-08-04T16:16:00.000000",
                    "totalVotes": 274033927,
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
                    "asrId": "2",
                    "proposalId": "CudfcXyY6JWKFkZxHMLv9ZvJuzBat4UvTx6anzW33TvM",
                    "proposalName": "Jupiter DAO: Microgrants Proposal",
                    "startDate": "2024-08-23T17:00:00.000000",
                    "endDate": "2024-08-27T17:00:00.000000",
                    "totalVotes": 267190808,
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
                    "asrId": "2",
                    "proposalId": "ApKpFDzwsjMEpW4zPNpmsHyPGfKrjaY6rA9HTLwV5a1w",
                    "proposalName": "Trial Budget: Jup & Juice WG (JJWG)",
                    "startDate": "2024-09-09T16:30:00.000000",
                    "endDate": "2024-09-12T16:30:00.000000",
                    "totalVotes": 256001468,
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
                    "asrId": "2",
                    "proposalId": "5G3ut22wiUWAoSnHCNTHus8LJTcnUaJKzjH1j1vLvoKs",
                    "proposalName": "J4J #2: Utilize Excess Jupuary for ASR",
                    "startDate": "2024-09-27T16:30:00.000000",
                    "endDate": "2024-10-01T16:30:00.000000",
                    "totalVotes": 307483434,
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
                    "asrId": "3",
                    "proposalId": "PJVgLKqBa5LabApp9uU5rvxUgqp4RdUfBxVbEddLxWa",
                    "proposalName": "Proposal: Increase Quorum for Jupiter DAO",
                    "startDate": "2024-10-25T16:31:00.000000",
                    "endDate": "2024-10-29T15:31:00.000000",
                    "totalVotes": 360642471,
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
                    "asrId": "3",
                    "proposalId": "ByQ21v3hqdQVwPHsfwurrtEAH8pB3DYuLdp9jU2Hwnd4",
                    "proposalName": "JUP Mobile Background Vote",
                    "startDate": 1731772799,
                    "endDate": 1732118399,
                    "totalVotes": 362217046,
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
                    "asrId": "3",
                    "proposalId": "CWAwYcLmniqQYnzDh3QGRH6FtymBesJ9dzk1EBvYNBwK",
                    "proposalName": "J4J #3: Jupuary Vote 1",
                    "startDate": 1732550399,
                    "endDate": 1732895999,
                    "totalVotes": 364576672,
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
                    "asrId": "3",
                    "proposalId": "xMLsw7zzBfRXNiQQo42aUohRsibgrmWcPt2mD8HdUUr",
                    "proposalName": "J4J #3: Jupuary Vote 2",
                    "startDate": 1733284800,
                    "endDate": 1733630400, # 1740067199
                    "totalVotes": 360223503,
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
                    "asrId": "4",
                    "proposalId": "8DA1TFPjbyfJXmQMrqRcQCGheoordFZ2fWNd3zpEhj2k",
                    "proposalName": "Proposal: Update Jupiter Logo",
                    "startDate": 1740584520,
                    "endDate": 1740930120,
                    "totalVotes": 453175767,
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Yes: Update the new logo to the Catstanbul themed logo.",
                            "title": "Yes"
                        },
                        {
                            "side": 2,
                            "name": "No: Maintain the existing logo, and revisit this later.",
                            "title": "No"
                        },
                    ]
                },
            ],
            "activeProposal": [
                {
                    "asrId": "4",
                    "proposalId": "8DA1TFPjbyfJXmQMrqRcQCGheoordFZ2fWNd3zpEhj2k",
                    "proposalName": "Proposal: Update Jupiter Logo",
                    "startDate": 1740584520,
                    "endDate": 1740930120,
                    "totalVotes": 453175767,
                    "proposalChoices": [
                        {
                            "side": 1,
                            "name": "Yes: Update the new logo to the Catstanbul themed logo.",
                            "title": "Yes"
                        },
                        {
                            "side": 2,
                            "name": "No: Maintain the existing logo, and revisit this later.",
                            "title": "No"
                        },
                    ]
                }],
            "asrs": [{
                "id": "1",
                "period": "March - June 2024",
                "rewards": {
                    "totalAsrRewards": [
                        {
                            "name": "Staked Jupiter",
                            "symbol": "JUP",
                            "value": 50000000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/JUP.webp",
                            "logic": {
                                "CqMsFvvmzETwwa2tXMZ75aNvjc5xy7VamxYC5u7v1ScA": 1.0,
                                "6txWyf3guJrhnNJXcAHxnV2oVxBcvebuSbfYsgB3yUKc": 1.0,
                                "5N9UbMGzga3SL8Rq7qDZCGfZX3FRDUhgqkSY2ksQjg8r": 1.0,
                                "2c2Yg1E9BNQVxqg9ZpB2CTBa4GGT8CoeWH6JN7ZQ5FDw": 1.0,
                                "A37zp1811aYLd7uoXN78KG12csC9dycyJcK7dD3R22zo": 0.333,
                                "DhJAwGDtHYdEy8mBoeZ3Yub5potxRJbvzycYUwhFGfox": 0.333,
                                "5QTT1AFSMA76dNUFYETiEAo54q3vKvGc8WexTGjamHDN": 0.333,
                                "GiPupbvjySF8XQr7NPk8z3HhLkkreuZ7pdDqcyaSWMXN": 1.0,
                                "CioyJmzFuRbN3Pda1LhvNxsEDoA4gQfTJ56F2hgWib5C": 1.0,
                            },
                        },
                        {
                            "name": "Zeus",
                            "symbol": "ZEUS",
                            "value": 7500000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/ZEUS.webp",
                            "logic": {
                                "CqMsFvvmzETwwa2tXMZ75aNvjc5xy7VamxYC5u7v1ScA": 1.0,
                                "6txWyf3guJrhnNJXcAHxnV2oVxBcvebuSbfYsgB3yUKc": 1.0,
                                "5N9UbMGzga3SL8Rq7qDZCGfZX3FRDUhgqkSY2ksQjg8r": 1.0,
                                "2c2Yg1E9BNQVxqg9ZpB2CTBa4GGT8CoeWH6JN7ZQ5FDw": 1.0,
                                "A37zp1811aYLd7uoXN78KG12csC9dycyJcK7dD3R22zo": 0.333,
                                "DhJAwGDtHYdEy8mBoeZ3Yub5potxRJbvzycYUwhFGfox": 0.333,
                                "5QTT1AFSMA76dNUFYETiEAo54q3vKvGc8WexTGjamHDN": 0.333,
                                "GiPupbvjySF8XQr7NPk8z3HhLkkreuZ7pdDqcyaSWMXN": 1.0,
                                "CioyJmzFuRbN3Pda1LhvNxsEDoA4gQfTJ56F2hgWib5C": 1.0,
                            },
                        },
                        {
                            "name": "WEN",
                            "symbol": "WEN",
                            "value": 7500000000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/WEN.webp",
                            "logic": {
                                "CqMsFvvmzETwwa2tXMZ75aNvjc5xy7VamxYC5u7v1ScA": 1.0,
                                "6txWyf3guJrhnNJXcAHxnV2oVxBcvebuSbfYsgB3yUKc": 1.0,
                                "5N9UbMGzga3SL8Rq7qDZCGfZX3FRDUhgqkSY2ksQjg8r": 1.0,
                                "2c2Yg1E9BNQVxqg9ZpB2CTBa4GGT8CoeWH6JN7ZQ5FDw": 1.0,
                                "A37zp1811aYLd7uoXN78KG12csC9dycyJcK7dD3R22zo": 0.333,
                                "DhJAwGDtHYdEy8mBoeZ3Yub5potxRJbvzycYUwhFGfox": 0.333,
                                "5QTT1AFSMA76dNUFYETiEAo54q3vKvGc8WexTGjamHDN": 0.333,
                                "GiPupbvjySF8XQr7NPk8z3HhLkkreuZ7pdDqcyaSWMXN": 1.0,
                                "CioyJmzFuRbN3Pda1LhvNxsEDoA4gQfTJ56F2hgWib5C": 1.0,
                            },
                        },
                        {
                            "name": "UPT",
                            "symbol": "UPT",
                            "value": 7500000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/UPT.webp",
                            "logic": {
                                "CqMsFvvmzETwwa2tXMZ75aNvjc5xy7VamxYC5u7v1ScA": 1.0,
                                "6txWyf3guJrhnNJXcAHxnV2oVxBcvebuSbfYsgB3yUKc": 1.0,
                                "5N9UbMGzga3SL8Rq7qDZCGfZX3FRDUhgqkSY2ksQjg8r": 1.0,
                                "2c2Yg1E9BNQVxqg9ZpB2CTBa4GGT8CoeWH6JN7ZQ5FDw": 1.0,
                                "A37zp1811aYLd7uoXN78KG12csC9dycyJcK7dD3R22zo": 0.333,
                                "DhJAwGDtHYdEy8mBoeZ3Yub5potxRJbvzycYUwhFGfox": 0.333,
                                "5QTT1AFSMA76dNUFYETiEAo54q3vKvGc8WexTGjamHDN": 0.333,
                                "GiPupbvjySF8XQr7NPk8z3HhLkkreuZ7pdDqcyaSWMXN": 1.0,
                                "CioyJmzFuRbN3Pda1LhvNxsEDoA4gQfTJ56F2hgWib5C": 1.0,
                            },
                        },
                        {
                            "name": "Shark",
                            "symbol": "SHARK",
                            "value": 750000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/SHARK.webp",
                            "logic": {
                                "CqMsFvvmzETwwa2tXMZ75aNvjc5xy7VamxYC5u7v1ScA": 1.0,
                                "6txWyf3guJrhnNJXcAHxnV2oVxBcvebuSbfYsgB3yUKc": 1.0,
                                "5N9UbMGzga3SL8Rq7qDZCGfZX3FRDUhgqkSY2ksQjg8r": 1.0,
                                "2c2Yg1E9BNQVxqg9ZpB2CTBa4GGT8CoeWH6JN7ZQ5FDw": 1.0,
                                "A37zp1811aYLd7uoXN78KG12csC9dycyJcK7dD3R22zo": 0.333,
                                "DhJAwGDtHYdEy8mBoeZ3Yub5potxRJbvzycYUwhFGfox": 0.333,
                                "5QTT1AFSMA76dNUFYETiEAo54q3vKvGc8WexTGjamHDN": 0.333,
                                "GiPupbvjySF8XQr7NPk8z3HhLkkreuZ7pdDqcyaSWMXN": 1.0,
                                "CioyJmzFuRbN3Pda1LhvNxsEDoA4gQfTJ56F2hgWib5C": 1.0,
                            },
                        },
                    ]
                }
            }, {
                "id": "2",
                "period": "July - September 2024",
                "rewards": {
                    "totalAsrRewards": [
                        {
                            "name": "Staked Jupiter",
                            "symbol": "JUP",
                            "value": 50000000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/JUP.webp",
                            "logic": {
                                "CnzPx1KQu1SFvGJHpZ4ykNkmfHSLBKx1oVESyjb5CjYC": 1.0,
                                "CudfcXyY6JWKFkZxHMLv9ZvJuzBat4UvTx6anzW33TvM": 1.0,
                                "ApKpFDzwsjMEpW4zPNpmsHyPGfKrjaY6rA9HTLwV5a1w": 1.0,
                                "5G3ut22wiUWAoSnHCNTHus8LJTcnUaJKzjH1j1vLvoKs": 1.0,
                            },

                        },
                        {
                            "name": "Cloud",
                            "symbol": "CLOUD",
                            "value": 7500000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/CLOUD.webp",
                            "logic": {
                                "2c2Yg1E9BNQVxqg9ZpB2CTBa4GGT8CoeWH6JN7ZQ5FDw": 1.0,
                                "CnzPx1KQu1SFvGJHpZ4ykNkmfHSLBKx1oVESyjb5CjYC": 1.0,
                                "CudfcXyY6JWKFkZxHMLv9ZvJuzBat4UvTx6anzW33TvM": 1.0,
                                "ApKpFDzwsjMEpW4zPNpmsHyPGfKrjaY6rA9HTLwV5a1w": 1.0,
                                "5G3ut22wiUWAoSnHCNTHus8LJTcnUaJKzjH1j1vLvoKs": 1.0,
                            },
                        },
                    ]
                }
            }, {
                "id": "3",
                "period": "October - December 2024",
                "rewards": {
                    "totalAsrRewards": [
                        {
                            "name": "Staked Jupiter",
                            "symbol": "JUP",
                            "value": 50000000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/JUP.webp",
                            "logic": {
                                "PJVgLKqBa5LabApp9uU5rvxUgqp4RdUfBxVbEddLxWa": 1.0,
                                "ByQ21v3hqdQVwPHsfwurrtEAH8pB3DYuLdp9jU2Hwnd4": 1.0,
                                "CWAwYcLmniqQYnzDh3QGRH6FtymBesJ9dzk1EBvYNBwK": 1.0,
                                "xMLsw7zzBfRXNiQQo42aUohRsibgrmWcPt2mD8HdUUr": 1.0,
                            },
                        },
                        {
                            "name": "deBridge",
                            "symbol": "DBR",
                            "value": 75000000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/DBR.webp",
                            "logic": {
                                "GiPupbvjySF8XQr7NPk8z3HhLkkreuZ7pdDqcyaSWMXN": 1.0,
                                "PJVgLKqBa5LabApp9uU5rvxUgqp4RdUfBxVbEddLxWa": 1.0,
                                "ByQ21v3hqdQVwPHsfwurrtEAH8pB3DYuLdp9jU2Hwnd4": 1.0,
                                "CWAwYcLmniqQYnzDh3QGRH6FtymBesJ9dzk1EBvYNBwK": 1.0,
                                "xMLsw7zzBfRXNiQQo42aUohRsibgrmWcPt2mD8HdUUr": 1.0,
                            },
                        },
                    ]
                }
            }, {
                "id": "4",
                "period": "January - March 2025",
                "rewards": {
                    "totalAsrRewards": [
                        {
                            "name": "Staked Jupiter",
                            "symbol": "JUP",
                            "value": 50000000,
                            "logoUrl": "https://d2l35o8v06vi7z.cloudfront.net/JUP.webp",
                            "logic": {
                                "8DA1TFPjbyfJXmQMrqRcQCGheoordFZ2fWNd3zpEhj2k": 1.0,
                            },
                        },
                    ]
                }
            }]
        }),
    }
