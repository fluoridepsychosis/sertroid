# Sertroid

Sertroid is a small, simple set of scripts which queries the Tripsit factsheet API in order to acquire a list of drug names.

It then takes these drug names and searches for scientific papers which have been cited on the Pubmed database that day which contain those drug names, and obtains some relevant summary data and urls for those papers using the Entrez E-utilities service.

It then outputs this information into an IRC channel on the Tripsit network. Sertroid runs on Tripsit once per 24hrs at 00:00 UTC.

The purpose of this program is to make it very easy for users of the network to keep up to date with the latest science on psychoactive substances of all kinds.

It is called Sertroid because I have written it while zonked on sertraline.
