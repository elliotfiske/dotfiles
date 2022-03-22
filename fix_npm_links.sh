{
	cd ~/repo/airkit/node/cxr
	npm link
}

{
	(cd ~/repo/airkit/node/web-builder && npm install && npm link @ruist/cxr) &
	(cd ~/repo/airkit/node/session-gateway && npm install && npm link @ruist/cxr)
}

{
	cd ~/repo/airkit/node/cxr &&
	npm install && npm start
}