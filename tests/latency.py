import asyncio
import httpx
import time
import os
import statistics
import random

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/chat")

BASE_MESSAGES = [
    "J’ai une erreur 'paper jam' avec mon imprimante",
    "Mon PC affiche un écran bleu après une mise à jour",
    "Crée un ticket urgent pour Bob : imprimante ne se connecte plus au WiFi",
    "Mon logiciel de messagerie se ferme tout seul",
    "Connexion Wi-Fi instable",
    "Je n’arrive pas à me connecter à mon compte",
    "Ticket urgent : serveur en panne",
    "Le clavier ne répond plus",
    "Je ne reçois plus mes emails",
    "Comment changer mon mot de passe Windows ?"
]

TOTAL_REQUESTS = 10  # How many requests to send

async def send_request(client, session_id, message):
    data = {"messages": [{"role": "user", "content": message}]}
    start = time.time()
    r = await client.post(BACKEND_URL, json=data)
    latency = time.time() - start
    return session_id, r.status_code, latency

async def main():
    # Generate messages
    messages = [random.choice(BASE_MESSAGES) for _ in range(TOTAL_REQUESTS)]
    results = []

    start = time.time()
    async with httpx.AsyncClient(timeout=150.0) as client:
        for i, message in enumerate(messages):
            res = await send_request(client, f"s{i+1}", message)
            results.append(res)

    end = time.time()

    # Extract latencies
    latencies = [lat for _, _, lat in results]
    avg_latency = statistics.mean(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)
    total_time = end - start
    rps = len(results) / total_time

    # Print summary
    print("\n--- Résultats ---")
    print(f"Requêtes envoyées: {len(results)}")
    print(f"Temps total: {total_time:.2f}s")
    print(f"Latence moyenne: {avg_latency:.2f}s")
    print(f"Latence min: {min_latency:.2f}s")
    print(f"Latence max: {max_latency:.2f}s")
    print(f"Throughput: {rps:.2f} requêtes/sec")

if __name__ == "__main__":
    asyncio.run(main())
