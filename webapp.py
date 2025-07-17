import os
from flask import Flask, render_template_string, jsonify, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

def generate_secret(p):
    secret_counter = session.get('secret_counter', 4)
    session['secret_counter'] = secret_counter + 3
    return secret_counter

def generate_public_key(alpha, secret, p):
    return pow(alpha, secret, p)

def calculate_shared_key(their_public_key, my_secret, p):
    return pow(their_public_key, my_secret, p)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diffie-Hellman MitM Attack Simulator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .card-enter {
            opacity: 0;
            transform: translateY(20px);
            animation: fadeIn 0.5s forwards;
        }
        @keyframes fadeIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .value-box {
            background-color: #f3f4f6; /* gray-100 */
            border: 1px solid #d1d5db; /* gray-300 */
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem; /* rounded-md */
            font-family: monospace;
            word-break: break-all;
            min-height: 42px;
            display: flex;
            align-items: center;
        }
        .status-box {
            transition: all 0.3s ease-in-out;
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">

    <div class="container mx-auto p-4 md:p-8">
        <header class="text-center mb-8">
            <h1 class="text-3xl md:text-4xl font-bold text-gray-900">Diffie-Hellman Man-in-the-Middle Attack</h1>
            <p class="mt-2 text-lg text-gray-600">An interactive simulation of how Eve can intercept a key exchange.</p>
        </header>

        <!-- Controls and Status -->
        <div class="bg-white p-6 rounded-xl shadow-lg mb-8 border border-gray-200">
             <div class="flex flex-wrap gap-4 justify-center items-center">
                <button id="btn-init" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors shadow">1. Initialize (p, α)</button>
                <button id="btn-generate-secrets" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors shadow" disabled>2. Generate All Secrets</button>
                <button id="btn-exchange-public" class="bg-purple-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-purple-700 transition-colors shadow" disabled>3. Exchange Public Keys</button>
                <button id="btn-compute-shared" class="bg-teal-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-teal-700 transition-colors shadow" disabled>4. Compute Shared Keys</button>
                <button id="btn-reset" class="bg-gray-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-gray-600 transition-colors shadow">Reset</button>
            </div>
            <div id="status" class="status-box text-center mt-6 p-4 bg-gray-100 rounded-lg text-gray-700 font-medium">
                Click "Initialize" to begin the simulation.
            </div>
        </div>

        <!-- Public Parameters -->
        <div id="public-params" class="text-center mb-8 hidden card-enter">
            <h2 class="text-2xl font-semibold mb-4">Public Parameters</h2>
            <div class="flex justify-center gap-8 bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                <div>
                    <h3 class="text-lg font-medium">Prime (p)</h3>
                    <div id="p-val" class="value-box mt-2 text-blue-600"></div>
                </div>
                <div>
                    <h3 class="text-lg font-medium">Generator (α)</h3>
                    <div id="alpha-val" class="value-box mt-2 text-blue-600"></div>
                </div>
            </div>
        </div>

        <!-- Alice, Eve, Bob columns -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

            <!-- Alice's Column -->
            <div id="alice-col" class="bg-white p-6 rounded-xl shadow-lg border border-green-200 hidden card-enter">
                <h2 class="text-2xl font-bold text-center text-green-700">Alice</h2>
                <div class="mt-4 space-y-4">
                    <div>
                        <label class="font-semibold">Secret Key (S<sub>A</sub>):</label>
                        <div id="alice-secret" class="value-box text-green-800"></div>
                    </div>
                    <div>
                        <label class="font-semibold">Her Public Key (T<sub>A</sub>):</label>
                        <p class="text-sm text-gray-500">α<sup>S<sub>A</sub></sup> mod p</p>
                        <div id="alice-public" class="value-box text-green-800"></div>
                    </div>
                    <div>
                        <label class="font-semibold">Received Public Key:</label>
                        <p class="text-sm text-gray-500">(Actually from Eve)</p>
                        <div id="alice-received-key" class="value-box text-red-600"></div>
                    </div>
                    <div>
                        <label class="font-semibold">Computed Shared Key (K<sub>A</sub>):</label>
                        <p class="text-sm text-gray-500">T<sub>Received</sub><sup>S<sub>A</sub></sup> mod p</p>
                        <div id="alice-shared-key" class="value-box font-bold text-xl text-green-800"></div>
                    </div>
                </div>
            </div>

            <!-- Eve's Column -->
            <div id="eve-col" class="bg-white p-6 rounded-xl shadow-lg border border-red-200 hidden card-enter">
                <h2 class="text-2xl font-bold text-center text-red-700">Eve (The Attacker)</h2>
                <div class="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-4">
                    <div>
                        <label class="font-semibold">Secret for Alice (S<sub>EA</sub>):</label>
                        <div id="eve-secret-a" class="value-box text-red-800"></div>
                    </div>
                     <div>
                        <label class="font-semibold">Secret for Bob (S<sub>EB</sub>):</label>
                        <div id="eve-secret-b" class="value-box text-red-800"></div>
                    </div>
                    <div>
                        <label class="font-semibold">Public Key for Alice (T<sub>EA</sub>):</label>
                        <div id="eve-public-a" class="value-box text-red-800"></div>
                    </div>
                    <div>
                        <label class="font-semibold">Public Key for Bob (T<sub>EB</sub>):</label>
                        <div id="eve-public-b" class="value-box text-red-800"></div>
                    </div>
                </div>
                <div class="mt-4 border-t pt-4">
                     <p class="text-center font-semibold mb-2">Eve's Interception & Computed Keys</p>
                     <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-4">
                        <div>
                            <label class="font-semibold">Key with Alice (K<sub>EA</sub>):</label>
                            <div id="eve-key-a" class="value-box font-bold text-xl text-red-800"></div>
                        </div>
                        <div>
                            <label class="font-semibold">Key with Bob (K<sub>EB</sub>):</label>
                            <div id="eve-key-b" class="value-box font-bold text-xl text-red-800"></div>
                        </div>
                     </div>
                </div>
            </div>

            <!-- Bob's Column -->
            <div id="bob-col" class="bg-white p-6 rounded-xl shadow-lg border border-blue-200 hidden card-enter">
                <h2 class="text-2xl font-bold text-center text-blue-700">Bob</h2>
                 <div class="mt-4 space-y-4">
                    <div>
                        <label class="font-semibold">Secret Key (S<sub>B</sub>):</label>
                        <div id="bob-secret" class="value-box text-blue-800"></div>
                    </div>
                    <div>
                        <label class="font-semibold">His Public Key (T<sub>B</sub>):</label>
                         <p class="text-sm text-gray-500">α<sup>S<sub>B</sub></sup> mod p</p>
                        <div id="bob-public" class="value-box text-blue-800"></div>
                    </div>
                    <div>
                        <label class="font-semibold">Received Public Key:</label>
                        <p class="text-sm text-gray-500">(Actually from Eve)</p>
                        <div id="bob-received-key" class="value-box text-red-600"></div>
                    </div>
                    <div>
                        <label class="font-semibold">Computed Shared Key (K<sub>B</sub>):</label>
                         <p class="text-sm text-gray-500">T<sub>Received</sub><sup>S<sub>B</sub></sup> mod p</p>
                        <div id="bob-shared-key" class="value-box font-bold text-xl text-blue-800"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Verification Result -->
        <div id="verification" class="text-center mt-8 hidden card-enter">
             <h2 class="text-2xl font-semibold mb-4">Verification</h2>
             <div id="verification-box" class="bg-white p-6 rounded-xl shadow-lg border-2">
                 <!-- Content will be injected by JS -->
             </div>
        </div>

    </div>

    <script>
        // --- DOM Element References ---
        const elements = {
            pVal: document.getElementById('p-val'),
            alphaVal: document.getElementById('alpha-val'),
            aliceSecret: document.getElementById('alice-secret'),
            alicePublic: document.getElementById('alice-public'),
            aliceReceivedKey: document.getElementById('alice-received-key'),
            aliceSharedKey: document.getElementById('alice-shared-key'),
            bobSecret: document.getElementById('bob-secret'),
            bobPublic: document.getElementById('bob-public'),
            bobReceivedKey: document.getElementById('bob-received-key'),
            bobSharedKey: document.getElementById('bob-shared-key'),
            eveSecretA: document.getElementById('eve-secret-a'),
            eveSecretB: document.getElementById('eve-secret-b'),
            evePublicA: document.getElementById('eve-public-a'),
            evePublicB: document.getElementById('eve-public-b'),
            eveKeyA: document.getElementById('eve-key-a'),
            eveKeyB: document.getElementById('eve-key-b'),
            status: document.getElementById('status'),
            verificationBox: document.getElementById('verification-box'),
            publicParams: document.getElementById('public-params'),
            aliceCol: document.getElementById('alice-col'),
            eveCol: document.getElementById('eve-col'),
            bobCol: document.getElementById('bob-col'),
            verification: document.getElementById('verification'),
            btnInit: document.getElementById('btn-init'),
            btnGenerateSecrets: document.getElementById('btn-generate-secrets'),
            btnExchangePublic: document.getElementById('btn-exchange-public'),
            btnComputeShared: document.getElementById('btn-compute-shared'),
            btnReset: document.getElementById('btn-reset'),
        };

        // --- State Update Function ---
        function updateUI(state) {
            // This function takes the state from the server and updates the webpage.
            elements.pVal.textContent = state.p || '';
            elements.alphaVal.textContent = state.alpha || '';
            elements.aliceSecret.textContent = state.SA || '';
            elements.bobSecret.textContent = state.SB || '';
            elements.eveSecretA.textContent = state.SE_A || '';
            elements.eveSecretB.textContent = state.SE_B || '';
            elements.alicePublic.textContent = state.TA || '';
            elements.bobPublic.textContent = state.TB || '';
            elements.evePublicA.textContent = state.TE_A || '';
            elements.evePublicB.textContent = state.TE_B || '';
            elements.aliceReceivedKey.textContent = state.TA_received || '';
            elements.bobReceivedKey.textContent = state.TB_received || '';
            elements.aliceSharedKey.textContent = state.KeyA || '';
            elements.bobSharedKey.textContent = state.KeyB || '';
            elements.eveKeyA.textContent = state.KeyE_A || '';
            elements.eveKeyB.textContent = state.KeyE_B || '';
            
            // Show/hide sections based on state
            if (state.p) {
                elements.publicParams.classList.remove('hidden');
                elements.aliceCol.classList.remove('hidden');
                elements.eveCol.classList.remove('hidden');
                elements.bobCol.classList.remove('hidden');
            } else {
                elements.publicParams.classList.add('hidden');
                elements.aliceCol.classList.add('hidden');
                elements.eveCol.classList.add('hidden');
                elements.bobCol.classList.add('hidden');
                elements.verification.classList.add('hidden');
            }
            
            // Update button states
            elements.btnInit.disabled = state.step > 0;
            elements.btnGenerateSecrets.disabled = state.step !== 1;
            elements.btnExchangePublic.disabled = state.step !== 2;
            elements.btnComputeShared.disabled = state.step !== 3;

            // Update status message
            if (state.status) {
                elements.status.textContent = state.status;
            }
        }

        // --- Event Handlers ---
        async function handleAction(endpoint) {
            try {
                const response = await fetch(endpoint, { method: 'POST' });
                if (!response.ok) throw new Error('Network response was not ok');
                const state = await response.json();
                updateUI(state);
                // After the final step, run verification
                if (endpoint === '/compute_shared') {
                    verifyKeys();
                }
            } catch (error) {
                console.error('Error during fetch:', error);
                elements.status.textContent = 'An error occurred. Please check the console.';
            }
        }
        
        async function verifyKeys() {
            const response = await fetch('/verify', { method: 'GET' });
            const result = await response.json();
            
            elements.verification.classList.remove('hidden');
            elements.verificationBox.innerHTML = ''; // Clear previous results
            
            // Alice vs Bob
            const aliceBobMatch = result.alice_bob_match;
            const abDiv = document.createElement('div');
            abDiv.className = `p-4 rounded-lg mb-4 text-white ${aliceBobMatch ? 'bg-green-600' : 'bg-red-600'}`;
            abDiv.innerHTML = `
                <h3 class="font-bold text-lg">Alice's Key vs Bob's Key</h3>
                <p>Match: <span class="font-extrabold">${aliceBobMatch ? 'YES! (Attack Succeeded)' : 'NO'}</span></p>
                <p class="mt-1">Alice and Bob think they have a secure channel, but their keys do not match. They are both communicating with Eve instead.</p>
            `;
            elements.verificationBox.appendChild(abDiv);
            
            // Alice vs Eve
            const aliceEveMatch = result.alice_eve_match;
            const aeDiv = document.createElement('div');
            aeDiv.className = `p-4 rounded-lg mb-4 text-white ${aliceEveMatch ? 'bg-green-600' : 'bg-red-600'}`;
            aeDiv.innerHTML = `
                <h3 class="font-bold text-lg">Alice's Key vs Eve's Key for Alice</h3>
                <p>Match: <span class="font-extrabold">${aliceEveMatch ? 'YES' : 'NO'}</span></p>
                <p class="mt-1">Eve has successfully generated the same key as Alice. She can now decrypt all messages from Alice.</p>
            `;
            elements.verificationBox.appendChild(aeDiv);
            
            // Bob vs Eve
            const bobEveMatch = result.bob_eve_match;
            const beDiv = document.createElement('div');
            beDiv.className = `p-4 rounded-lg text-white ${bobEveMatch ? 'bg-green-600' : 'bg-red-600'}`;
            beDiv.innerHTML = `
                <h3 class="font-bold text-lg">Bob's Key vs Eve's Key for Bob</h3>
                <p>Match: <span class="font-extrabold">${bobEveMatch ? 'YES' : 'NO'}</span></p>
                <p class="mt-1">Eve has also generated the same key as Bob. She can decrypt all messages from Bob.</p>
            `;
            elements.verificationBox.appendChild(beDiv);
        }

        // --- Attach Event Listeners ---
        elements.btnInit.addEventListener('click', () => handleAction('/init'));
        elements.btnGenerateSecrets.addEventListener('click', () => handleAction('/generate_secrets'));
        elements.btnExchangePublic.addEventListener('click', () => handleAction('/exchange_public_keys'));
        elements.btnComputeShared.addEventListener('click', () => handleAction('/compute_shared'));
        
        elements.btnReset.addEventListener('click', async () => {
            await fetch('/reset', { method: 'POST' });
            // Reset UI to initial state
            updateUI({
                step: 0,
                status: 'Simulation reset. Click "Initialize" to begin again.'
            });
        });
        
        // Load initial state on page load
        document.addEventListener('DOMContentLoaded', async () => {
            const response = await fetch('/state');
            const state = await response.json();
            updateUI(state);
            if(state.step === 4) {
               verifyKeys();
            }
        });

    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/state')
def get_state():
    return jsonify(session.get('state', {'step': 0, 'status': 'Click "Initialize" to begin.'}))

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return jsonify({'status': 'ok'})

@app.route('/init', methods=['POST'])
def init_params():
    session.clear()
    p = 23
    alpha = 5
    state = {
        'p': p,
        'alpha': alpha,
        'step': 1,
        'status': 'Public parameters p and α have been established.'
    }
    session['state'] = state
    return jsonify(state)

@app.route('/generate_secrets', methods=['POST'])
def generate_secrets():
    state = session.get('state', {})
    if state.get('step') != 1:
        return jsonify({'error': 'Invalid step'}), 400

    p = state['p']
    
    state['SA'] = generate_secret(p)
    
    state['SB'] = generate_secret(p)
    
    state['SE_A'] = generate_secret(p)
    state['SE_B'] = generate_secret(p)
    
    state['step'] = 2
    state['status'] = 'Alice, Bob, and Eve have all generated their secret numbers.'
    session['state'] = state
    return jsonify(state)

@app.route('/exchange_public_keys', methods=['POST'])
def exchange_keys():
    state = session.get('state', {})
    if state.get('step') != 2:
        return jsonify({'error': 'Invalid step'}), 400
        
    p = state['p']
    alpha = state['alpha']

    state['TA'] = generate_public_key(alpha, state['SA'], p)
    state['TB'] = generate_public_key(alpha, state['SB'], p)
    
    state['TE_A'] = generate_public_key(alpha, state['SE_A'], p)
    state['TE_B'] = generate_public_key(alpha, state['SE_B'], p)
    
    state['TA_received'] = state['TE_A']
    state['TB_received'] = state['TE_B']
    
    state['step'] = 3
    state['status'] = "Alice & Bob sent public keys. Eve intercepted them and sent her own instead!"
    session['state'] = state
    return jsonify(state)

@app.route('/compute_shared', methods=['POST'])
def compute_shared():
    state = session.get('state', {})
    if state.get('step') != 3:
        return jsonify({'error': 'Invalid step'}), 400
        
    p = state['p']
    
    state['KeyA'] = calculate_shared_key(state['TA_received'], state['SA'], p)
    
    state['KeyB'] = calculate_shared_key(state['TB_received'], state['SB'], p)
    
    state['KeyE_A'] = calculate_shared_key(state['TA'], state['SE_A'], p)
    state['KeyE_B'] = calculate_shared_key(state['TB'], state['SE_B'], p)
    
    state['step'] = 4
    state['status'] = 'All parties have computed their shared keys. Now, verify the results.'
    session['state'] = state
    return jsonify(state)

@app.route('/verify')
def verify():
    state = session.get('state', {})
    if state.get('step') != 4:
        return jsonify({'error': 'Keys not computed yet'}), 400
        
    results = {
        'alice_bob_match': state['KeyA'] == state['KeyB'],
        'alice_eve_match': state['KeyA'] == state['KeyE_A'],
        'bob_eve_match': state['KeyB'] == state['KeyE_B']
    }
    return jsonify(results)

if __name__ == '__main__':
    # http://127.0.0.1:5000
    app.run(debug=True)

