# Guide de Déploiement & Monétisation : Conway Automaton

Ce guide résume la configuration prête à l'emploi mise en place dans cet environnement pour lancer un agent autonome avec une stratégie de rentabilisation sur un budget de 100 $.

---

## 1. Ce qui est déjà prêt sur la machine

* **Code source compilé** : `/workspace/automaton` (Node.js 22, TypeScript, Viem, Better-SQLite3).
* **Portefeuille de l'agent généré** :
  * **Adresse sur Base** : `0x959D888A46b870EBa0046Fe3588b1422e0C22B48`
  * **Clé privée** : stockée de manière sécurisée sous `~/.automaton/wallet.json` (permissions `0600`).
* **Invariants installés sous `~/.automaton/`** :
  * `constitution.md` (protégé en lecture seule `0444`, immuable par l'agent).
  * `heartbeat.yml` (planification des réveils et contrôles d'état).
  * `SOUL.md` (identité initiale).
  * `skills/` (modules `conway-compute`, `conway-payments`, `survival`).

---

## 2. Configuration économique recommandée

Pour éviter que l'agent ne dilapide vos 100 $ en appels LLM futiles, créez votre fichier `~/.automaton/automaton.json` avec des garde-fous stricts :

```json
{
  "name": "BaseSentinel",
  "genesisPrompt": "Tu es BaseSentinel, une API de sécurité et d'analyse de contrats intelligents sur Base. Tu exposes sur le port 8080 un endpoint HTTP sécurisé avec le protocole x402 facturé 0.25 USDC par requête. En échange du paiement, tu analyses l'adresse du smart contract fourni et retournes un rapport de risques en JSON. Tu dois préserver ta réserve financière, désactiver les sous-agents (maxChildren: 0) et maximiser tes profits en USDC.",
  "creatorAddress": "VOTRE_ADRESSE_BASE_PERSONNELLE",
  "registeredWithConway": false,
  "sandboxId": "",
  "conwayApiUrl": "https://api.conway.tech",
  "conwayApiKey": "",
  "inferenceModel": "gpt-4.1-mini",
  "maxTokensPerTurn": 2048,
  "heartbeatConfigPath": "~/.automaton/heartbeat.yml",
  "dbPath": "~/.automaton/state.db",
  "logLevel": "info",
  "walletAddress": "0x959D888A46b870EBa0046Fe3588b1422e0C22B48",
  "version": "0.2.1",
  "skillsDir": "~/.automaton/skills",
  "maxChildren": 0,
  "maxTurnsPerCycle": 15,
  "childSandboxMemoryMb": 512,
  "treasuryPolicy": {
    "maxSingleTransferCents": 1000,
    "maxHourlyTransferCents": 2000,
    "maxDailyTransferCents": 5000,
    "minimumReserveCents": 1000,
    "maxX402PaymentCents": 100,
    "x402AllowedDomains": ["conway.tech"],
    "transferCooldownMs": 60000,
    "maxTransfersPerTurn": 1,
    "maxInferenceDailyCents": 1000,
    "requireConfirmationAboveCents": 1000
  },
  "chainType": "evm"
}
```

---

## 3. Déploiement et Démarrage par Paliers

### Palier 1 : Test à 25 $ (Recommandé)
1. Ouvrez votre portefeuille crypto (Metamask, Rabby...).
2. Envoyez **25 $ USDC** sur le réseau **Base** à l'adresse de l'agent :
   ```
   0x959D888A46b870EBa0046Fe3588b1422e0C22B48
   ```
3. Envoyez également **0.001 ETH sur Base** (~2 à 3 $) pour couvrir les frais de gaz des transferts.
4. Lancez l'agent :
   ```bash
   cd /workspace/automaton
   node dist/index.js --run
   ```

### Palier 2 : Vérification du statut et de la trésorerie
Dans un second terminal :
```bash
# Vérifier l'état et le solde de l'agent :
node /workspace/automaton/packages/cli/dist/index.js status

# Surveiller les logs d'activité en direct :
node /workspace/automaton/packages/cli/dist/index.js logs --tail 30
```

### Palier 3 : Validation du service payant
Faites un appel test à l'API x402 de l'agent pour vérifier qu'il encaisse bien 0.25 USDC et fournit le service. Dès que le canal de vente est validé, vous pouvez injecter les 75 $ restants pour lui donner jusqu'à 2 mois d'autonomie complète.
