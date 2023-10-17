# LATIA112-1 HW01

## Virtual Environment
Recommend to use venv to isolate you environment.

```bash
$ python3.11 -m venv venv
$ source venv/bin/activate
```

## Dependancy

```bash
$ pip install -r requirements.txt
```

## Material
* [Career Development Support and Educational Practices in Universities: A Discussion of Educational Effectiveness of Internship in Enterprises from the Perspective of Cross-Boundary Learning](https://srda.sinica.edu.tw/datasearch_detail.php?id=3016)

### Change SAV File to CSV File
I use [spss-converter](https://github.com/insightindustry/spss-converter) to solve it.

* python code utilize spss-converter
    * ```python
        from spss_converter import read

        read.to_csv('data.sav',target = 'file.csv')
        ```

* requirement.txt
    * The spss-converter is never update, so pandas version might not upgrade the the newset version, or it will cause [line_terminator error](https://stackoverflow.com/questions/43684096/pandas-to-csv-got-an-unexpected-keyword-argument).
    * ```txt
        pandas==1.2.0
        pyreadstat>=1.0.6
        PyYAML==5.3.1
        simplejson==3.17.2
        validator-collection>=1.5.0
        openpyxl>=3.0.7
        ```