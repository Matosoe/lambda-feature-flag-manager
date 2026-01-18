#!/bin/bash

echo "🔄 Reiniciando ambiente..."
echo ""

./down.sh
sleep 2
./up.sh
