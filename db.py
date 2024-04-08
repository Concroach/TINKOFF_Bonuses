import psycopg
import asyncio

class Database:
    def __init__(self):
        print("init")

    async def async_init(self):
        self.connection = await psycopg.AsyncConnection.connect(user='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', 
                                                    password='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', 
                                                    dbname='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX', 
                                                    host='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX',
                                                    port='XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX')
        self.cursor = self.connection.cursor() 
    
    async def user_exists(self, user_id):
        await self.cursor.execute(f"""SELECT * FROM Users WHERE Users.user_id = '{user_id}'""")
        result = await self.cursor.fetchone()
        return result
            
    async def add_user(self, user_id, username):
        await self.cursor.execute(f"""INSERT INTO users (user_id) VALUES('{user_id}');""")
        await self.cursor.execute(f"""UPDATE users SET username = '{username}' WHERE user_id = '{user_id}';""")
        await self.connection.commit()
    
    async def delete_user(self, user_id):
        await self.cursor.execute(f"""DELETE FROM Users WHERE user_id = '{user_id}'""")
        await self.connection.commit()
    
    async def get_all_users(self):
        await self.cursor.execute("SELECT user_id FROM users WHERE mailing_status = True")
        rows = await self.cursor.fetchall()
        user_ids = [row[0] for row in rows]
        return user_ids
    
    async def count_users(self):
        await self.cursor.execute("SELECT * FROM users")
        count = await self.cursor.fetchall()
        print(len(count))
        return len(count)

    async def add_mailing_status(self, user_id, status):
        await self.cursor.execute(f"""UPDATE Users SET mailing_status = '{status}' WHERE user_id = {user_id}""")
        await self.connection.commit()
        
    async def check_mailing_status(self, user_id):
        await self.cursor.execute(f"""SELECT mailing_status FROM Users WHERE Users.user_id = '{user_id}'""")
        result = await self.cursor.fetchone()
        return result[0]
    
    async def add_products(self, data):
        await self.cursor.execute('DELETE FROM bonuses')
        await self.connection.commit()

        for key, value in data.items():
            await self.cursor.execute('''
                INSERT INTO bonuses (id, advertTextHtml, merchantName, openDate, closeDate, cashbackPercent, new)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (key, value['advertTextHtml'], value['merchantName'], value['openDate'],
                value['closeDate'], value['cashbackPercent'], value['new']))

            await self.connection.commit()

    async def take_names_and_precents(self):
        await self.cursor.execute("SELECT id, merchantname, cashbackpercent, closedate FROM bonuses")
        result = await self.cursor.fetchall()
        
        python_array = [{'id': row[0], 'merchantname': row[1], 'cashbackpercent': row[2], 'closedate': row[3]} for row in result]
        
        sorted_array = sorted(python_array, key=lambda x: x['cashbackpercent'], reverse=True)
        
        return sorted_array

    async def take_all_ids(self):
        await self.cursor.execute("SELECT id FROM bonuses")
        result = await self.cursor.fetchall()
        
        id_array = [str(row[0]) for row in result]

        return id_array

    async def get_product_by_id(self, product_id):
        await self.cursor.execute("SELECT * FROM bonuses WHERE id = %s", (product_id,))
        result = await self.cursor.fetchone()
        print(result)
        if result:
            product_info = {
                'id': result[0],
                'adverttexthtml': result[1],
                'merchantname': result[2],
                'opendate': result[3],
                'closedate': result[4],
                'cashpercent': result[5],
                'new': result[6],
            }
            return product_info
        return None

    async def get_only_new_products(self):
        await self.cursor.execute("SELECT id, adverttexthtml, merchantname, opendate, closedate, cashbackpercent FROM bonuses WHERE new = True")

        rows = await self.cursor.fetchall()
        if rows:
            result_dict = {}
            for row in rows:
                id, adverttexthtml, merchantname, opendate, closedate, cashbackpercent = row
                result_dict[id] = {
                    "id": id,
                    "adverttexthtml": adverttexthtml,
                    "merchantname": merchantname,
                    "opendate": opendate,
                    "closedate": closedate,
                    "cashbackpercent": cashbackpercent
                }
            return result_dict
        return None