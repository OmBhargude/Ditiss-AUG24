from flask import Flask, render_template, request
import subprocess  # If you are using subprocess for subfinder

app = Flask(__name__)

DEBUG_PRINT = app.config['DEBUG_PRINT'] = True # Or however you set your debug flag

def enumerate_subdomains(domain):
    print(f"DEBUG: Starting subdomain enumeration for domain: {domain}") # ADDED LOGGING - START
    subdomains = []
    try:
        # Construct the subfinder command (adjust path if needed)
        command = ['./subfinder', '-d', domain, '-oJ'] # Assuming subfinder is in /app/subfinder and you want JSON output
        print(f"DEBUG: Executing command: {' '.join(command)}") # ADDED LOGGING - COMMAND

        process = subprocess.Popen(command, cwd='/app', stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Ensure cwd is /app if subfinder is there
        stdout, stderr = process.communicate()

        if stderr:
            error_message = stderr.decode()
            print(f"DEBUG: subfinder stderr: {error_message}") # ADDED LOGGING - STDERR
            return [], error_message # Return error message to display in frontend

        output = stdout.decode()
        print(f"DEBUG: subfinder stdout (raw): {output}") # ADDED LOGGING - STDOUT RAW

        # ... (Your code to parse the JSON output from subfinder and extract subdomains) ...
        # Example (you'll need to adapt this to your actual parsing logic):
        import json
        try:
            json_output = json.loads(output)
            if isinstance(json_output, list): # Assuming subfinder -oJ outputs a list of subdomains in JSON
                subdomains = [item for item in json_output if isinstance(item, str)] # Extract subdomain strings
                print(f"DEBUG: Extracted subdomains: {subdomains}") # ADDED LOGGING - EXTRACTED SUBDOMAINS
            else:
                print(f"DEBUG: Unexpected JSON output format from subfinder: {json_output}") # ADDED LOGGING - UNEXPECTED JSON FORMAT
                return [], "Unexpected output format from subfinder" # Handle unexpected format
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSONDecodeError: {e}") # ADDED LOGGING - JSON DECODE ERROR
            print(f"DEBUG: Raw output that caused JSONDecodeError: {output}") # ADDED LOGGING - RAW OUTPUT ON JSON ERROR
            return [], f"Error parsing subfinder output (JSONDecodeError): {e}"


    except FileNotFoundError:
        error_message = "Error: subfinder binary not found. Ensure it's in /app/subfinder and executable."
        print(f"DEBUG: FileNotFoundError: {error_message}") # ADDED LOGGING - FILENOTFOUND
        return [], error_message
    except Exception as e:
        error_message = f"An unexpected error occurred during subdomain enumeration: {e}"
        print(f"DEBUG: Exception: {error_message}") # ADDED LOGGING - GENERIC EXCEPTION
        return [], error_message

    print(f"DEBUG: Subdomain enumeration completed successfully. Found {len(subdomains)} subdomains.") # ADDED LOGGING - COMPLETION
    return subdomains, None # Return subdomains and no error

@app.route('/')
def index():
    domain = request.args.get('domain')
    subdomain_results = []
    error_message = None # Initialize error_message

    if domain:
        subdomain_results, error_message = enumerate_subdomains(domain) # Call your enumeration function

    return render_template('index.html', domain=domain, subdomain_results=subdomain_results, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=DEBUG_PRINT, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
