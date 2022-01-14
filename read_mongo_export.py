import re
import argparse

"""
    This file will help create a query to run agains Postgresql from the output of a MongoDb query.

    So, for MongoDb, after querying like this:
        db.getCollection('order').find({updateDate: {$gt: ISODate('2022-01-13 20:00:00'), $lt: ISODate('2022-01-14 08:00:00')}}, {odooId: true})

    and having an output similar to the one below:

   '''''''''''''''''''''''''''''''''

    ...
    /* 810 */
    {
        "_id" : ObjectId("61d436161b690f948c97d47a"),
        "odooId" : 61456
    }

    /* 811 */
    {
        "_id" : ObjectId("61d436161b690f948c97d47b"),
        "odooId" : 58355
    }
    ...

    '''''''''''''''''''''''''''''''''

    1. You can save it inside a textfile, and name it for example mongo_export.txt

    2. Then you can run this file like this:
        python read_mongo_export.py -i [your_mong_export.txt] -m odoo_model -f from_date -t to_date

        from_date and to_date should look something like this: '2022-01-13 20:00:00'

    3. This will generate a SQL query that you can run on Postgresql to fetch the same documents and explore them

"""



def main(args):
    regex = re.compile(r'"odooId" : (\d+)')
    with open(args.file, 'r') as mongo_export_file:
        file_content = mongo_export_file.read().replace('\n', '')
        result = regex.findall(file_content)
        if result:
            print("""
                SELECT id, create_date FROM {} WHERE
                id IN {} AND
                create_date >= '{}' AND
                create_date <= '{}';
            """.format(args.model, tuple(map(int,result)), args.date_from, args.date_to))
        else:
            print("Sorry, not odooId detected in file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file", default='mongo_export.txt')
    parser.add_argument("-m", "--model", required=True)
    parser.add_argument("-f", "--from", dest="date_from", required=True)
    parser.add_argument("-t", "--to", dest="date_to", required=True)
    args = parser.parse_args()

    main(args)
