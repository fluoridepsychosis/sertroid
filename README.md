# Sertroid

Sertroid is a small, simple set of scripts which queries the [Tripsit](https://tripsit.me/) factsheet [API](http://tripbot.tripsit.me/api/) in order to acquire a list of drug names.

It then takes these drug names and searches for scientific papers which have been cited on the [Pubmed database](https://www.ncbi.nlm.nih.gov/pubmed/) that day which contain those drug names, and obtains some relevant summary data and urls for those papers using the [Entrez E-utilities service](https://www.ncbi.nlm.nih.gov/books/NBK25497/).

It then outputs this information into a [channel](https://chat.tripsit.me/chat/?a=1&theme=dark&##paperflood) on the Tripsit IRC network. Sertroid runs on Tripsit once per 24hrs. It also outputs to a [website.](https://www.sertro.id)

The purpose of this program is to make it very easy for users of the network to keep up to date with the latest science on psychoactive substances of all kinds.

It is called Sertroid because I have written it while on sertraline.
