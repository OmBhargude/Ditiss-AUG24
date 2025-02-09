#!/bin/bash

# Function to resolve IP address(es) for a subdomain
resolve_ip() {
  subdomain="$1"
  ips=$(dig +short "$subdomain" A 2>/dev/null) # Get all IPs
  if [[ -z "$ips" ]]; then
    echo "NA"
  else
    echo "$ips" | tr '\n' ',' | sed 's/,$//' # Format IPs as comma-separated string
  fi
}


# Print header
printf "%-40s %-10s %-50s\n" "Subdomain" "Status" "IP Address(es)" # Wider IP column

# Run subfinder and process the output
./subfinder -d $1 -silent | while read subdomain; do
  status="Alive"
  ips=$(resolve_ip "$subdomain")

  if [[ "$ips" == "NA" ]]; then
    status="Dead"
  fi

  if [[ "$ips" == *"."* ]]; then  # Check if it contains a dot (likely an IP)
    printf "%-40s %-10s %-50s\n" "$subdomain" "$status" "$ips"
  else  # It's likely a CNAME
    cname="$ips"  # Store the CNAME
    resolved_ip=$(dig +short "$cname" A 2>/dev/null) # Resolve the CNAME

    if [[ -z "$resolved_ip" ]]; then # If CNAME cannot be resolved
      printf "%-40s %-10s %-50s\n" "$subdomain" "$status" "$cname" # Print just the CNAME
    else
      printf "%-40s %-10s %-50s\n" "$subdomain" "$status" "$resolved_ip ($cname)" # Print resolved IP and CNAME
    fi
  fi
done
