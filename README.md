# Booru Search

Search Danbooru with more than two tags

## Requirements

You should have Python 3, and some python modules installed (just run the following command if unsure):

```
pip3 install http3 urllib3 pybooru
```

## Usage

Add a line like this into the beginning of `booru-search.py` (preferably where the corresponding example is placed):
```
tags = [ 'kirisame_marisa', 'flandre_scarlet', 'kiss', '2girls' ]
```
(that was once the actual request from Yuka Kirabaki's Touhou Discord server lol).

You may specify as many tags as you want, but try to choose first two of them to be the hardest criterias.
For example, `[ 'hakurei_reimu', 'rumia', '2girls', 'simple_background' ]` is much better than `[ '2girls', 'simple_background', 'hakurei_reimu', 'rumia' ]`.
This is because they are used to get the search results from booru, and then each post from them are being tested for remaining tags.
In this example, first one gets you 86 pages of images, and second one gives more than 1000 pages (and danbooru is limiting your search on this number anyway).
FYI, each page is downloaded and tested for about one second, so try to make your search criteria stricter as possible with first two tags.

After you did that, just run `./booru-search.py`. It will show you how it traverses through pages of results of your request, and will finally generate a link to rentry website, where final results will be uploaded.
You can open this link, and check the resulting images.
Each image is the link to its danbooru page, and shows all its tags in a pop-up hint (title).

Also you may alter `booru` variable if you wish to work with another Danbooru mirror.

## Contributing

Feel free to post GitHub issues or pull requests, if you feel something is broken or missing.

Also feel free to use in your own free projects if you want.
