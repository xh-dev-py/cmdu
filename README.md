# Installation
```shell
pip install -U cmdu
```

# build
```shell
pip install -r requirements.txt
rm -rf dist
python -m build
python -m twine upload dist/* -u __token__ -p {token}
```
# Commands
```
|-- cmdu
|   |-- file-mod
|   |   |-- hosts
|   |   |   |-- add
|   |   |   |-- delete
|   |   |   |-- delete-all
|   |
|   |-- check-list
|   |   |-- create
|   |   |-- check
|   |   |-- uncheck
|   |
|   |-- lnes
|   |   |-- set-nu
|   |   |-- count
|   |   |-- skip
|   |   |-- filter
|   |   |-- filter-not
|   |
|   |-- convert
|   |   |-- j2j
|   |   |-- j2y
|   |   |-- y2j
|   |
```

## file-mod hosts add
add a host to specific ip
```shell
# input
127.0.0.1 abc.com

python -m cmdu file-mod hosts add -ip 127.0.0.1 -host abcx.com

# output
127.0.0.1 abc.com abcx.com
```

## file-mod hosts delete
delete a host from specific ip
```shell
# input
127.0.0.1 abc.com abcx.com

python -m cmdu file-mod hosts delete -ip 127.0.0.1 -host abcx.com

# output
127.0.0.1 abc.com
```

## file-mod hosts delete-all
delete all hosts from specific ip
```shell
# input
127.0.0.1 abc.com
127.0.0.2 abcx.com

python -m cmdu file-mod hosts delete-all -ip 127.0.0.2

# output
127.0.0.2 abcx.com
```


## check-list create
create line by line record to check list
```shell
# input
line 1
line 2

line 3

python -m cmdu check-list create

# output
[ ] 000001 |line 1
[ ] 000002 |line 2

[ ] 000003 |line 3
```

## check-list load
load check list from different format (simple, json, yaml) into other format (simple, json, yaml)
```shell
# input
[ ] 000001 |line 1
[x] 000002 |line 2

[X] 000003 |line 3

python -m cmdu check-list --simple-in --yaml-out

# out
- checked: false
  id: '000001'
  line: item 1
- checked: true
  id: '000002'
  line: item 2
- checked: true
  id: '000003'
  line: item 3
```

## check-lst check 
check the item by number 
```shell
# input
[ ] 000001 |line 1
[ ] 000002 |line 2

[ ] 000003 |line 3

python -m cmdu check-list check 2 3

# out
[ ] 000001 |line 1
[X] 000002 |line 2

[X] 000003 |line 3
```

## check-lst uncheck
uncheck the item by number
```shell
# input
[ ] 000001 |line 1
[x] 000002 |line 2

[X] 000003 |line 3

python -m cmdu check-list check 1 2 3

# out
[ ] 000001 |line 1
[ ] 000002 |line 2

[ ] 000003 |line 3
```

## lines set-nu
set line number to each line, pad `000000 |` to the left
1. `python -m cmdu lines set-nu`
    ```
    # input
    line 1
    line 2

    # output
    000001 |line 1
    000002 |line 2
    ```

## lines count
Count the number of lines
1. `python -m cmdu lines count`
    ```
    # input
    line 1
    line 2

    # output
    2
    ```

## lines skip
Skip the first n lines
1. `python -m cmdu lines skip 2`
    ```
    # input
    line 1
    line 2
    line 3

    # output
    line 3
    ```
   
## lines filter
Filter any match line
1. filter by regex, any matching in regex will make the whole line accepted
   ```shell
   # input
   line 1
   line 2
   line 3
   
   python -m cmdu filter --regex "^line 1$"
   
   # output
   line 1
   ```
   
## lines filter not
Filter any not match line
1. filter by regex, any matching in regex will make the whole line rejected
   ```shell
   # input
   line 1
   line 2
   line 3
   
   python -m cmdu filter-not --regex "^line 1$"
   
   # output
   line 2
   line 3
   ```

## convert j2j
convert a json input (from stdin) as json output (to stdout)
1. with raw json(no indentation and new line) `python -m cmdu json2json`
   ```shell
   # input
   {"a": 1, "b": 2}
   
   python-m cmdu json2json
   
   # output
   {"a": 1, "b": 2}
   ```
2. with pretty format `python -m cmdu json2json --pretty`
   ```shell
   # input
   {"a": 1, "b": 2}
   
   python-m cmdu json2json --pretty
   
    # output
    {
        "a": 1,
        "b": 2
    }
    ```
3. with pretty format and indentation as 2 `python -m cmdu json2json --pretty --indent 2`
    ```shell
    # input
    {"a": 1, "b": 2}
    
    python-m cmdu json2json --pretty --indent 2
    
    # output
    {
      "a": 1,
      "b": 2
    }
    ```

## convert j2y
convert a json input (from stdin) as yaml output (to stdout)
1. with json as yaml
    ```shell
    # input
    {"a": 1, "b": 2}
    
    python-m cmdu j2y
    
    # output
    a: 1
    b: 2
    ```

## convert y2j
convert a yaml input (from stdin) as json output (to stdout)
1. with raw json
   ```shell
   # input
   a: 1
   b: 2
   
   python-m cmdu y2j
   
   # output
   {"a": 1, "b": 2}
   ```
2. with pretty format `python -m cmdu yaml2json --pretty`
   ```shell
   # input
   a: 1
   b: 2
   
   python -m cmdu yaml2json --pretty
   
   # output
   {
        "a": 1,
        "b": 2
   }
    ```
3. with pretty format and indentation as 2 `python -m cmdu yaml2json --pretty --indent 2`
   ```shell
   # input
   a: 1
   b: 2
   
   python -m cmdu yaml2json --pretty --indent 2
   
   # output
   {
      "a": 1,
      "b": 2
   }
    ```
