# Stadtreinigung Hamburg

This library provides access to garbage collection dates
in Hamburg. It scrapes the official website of Stadtreinigung Hamburg,
so this library can break at any time. Please open an issue if the
library does not work anymore.

## Installation

Using pip:

```
sudo pip install stadtreinigung_hamburg
```

## Usage

After installing, use the terminal to run the program:

```
stadtreinigung_hamburg Sesamstraße 123
```


If your street name has a space, wrap the street in quotes:

```
stadtreinigung_hamburg "Sesame Street" 123
```


If you have problems with the street or street number,
use the official website and get the collection dates.
Then, search for `asId` and `hnId`. Those are the IDs for
your street and street number. You can use them too:

```
stadtreinigung_hamburg --asid 1234 --hnid 99999
```

Or mix it:

```
stadtreinigung_hamburg Sesamstraße --hnid 99999
```