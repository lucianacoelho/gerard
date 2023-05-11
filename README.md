# Aufredo
Aufredo is a module created to make Auth Rate analysis easier.

<mark style="background-color: #FFFF00">For now, Aufredo is optimized to work with data obtained from Braintree Gateway. Other data sources might work but not with all methods.</mark> 

# Import Aufredo

<pre><code>import sys
<br>sys.path.append(<path_t_module>)
<br>from <folder_name>.alfredo import alfredo
</code></pre>



# First, feed Aufredo the data:
> * Get the data from Braintree Gateway: Access https://login.braintreegateway.com/ >> Search for the Merchant you want to analyze >> Go to "Dashboard" > "Transactions" >> Filter the transactions as you please >> Click "search" at the bottom of the page >> Click "Download", wait for the processing and download the file.

# Then, instantiate:

>* alfredo(df, response_column, issuing_bank, not_deduped)<br>
<br>Args:<br>
df: str, the dataframe to be analyzed<br>
response_column: str, the column that returns whether the transaction was approved or not (usually returning the word 'Approved')<br>
issuing_bank: str, the column that returns the names of the Issuing Banks<br>
not_deduped (optional): boolean. Pass True to keep the original data and False to use deduped values.

E.g:
## deduped 
>* alfredo(df, 'Processor Response Text', 'Issuing Bank')

or

## not deduped 
>* alfredo(df, 'Processor Response Text', 'Issuing Bank', True)

# Aufredo has the following functionalities:

# report()
>* Returns Approval Rate (and the other 4 most commom responses) and the shares and impact of:<br>
    - Issuing Banks<br>
    - Card Networks<br>
    - Bins<br>
    - Descriptors<br>
    - Amount<br>
    - MAIDs<br>
    
>E.g: <br> <i>x.report()</i>
><br><br>Info: What is impact? Impact is how much the overall approval rate would go up if x had 100% approval.
<br>Example: Let's say Visa's impact is 5%, that means that 5% of the denied transactions from the overall operation (for Card Type only) come from VIsa. <b>It doesn't mean that Visa's approval rate is 95%, it means that if Visa's approval ever got to 100% the operation would increase in 5% approval.</b>
<br><br>And what is share? Share is how many % X represents from the overall operation.
<br>Example: If Visa's share is 38%, that means that, looking only for Card Types, 38% of all the transactions from the Merchant are Visa cards.

# decline()
> Top x that are declining more.
<br>Args: 
<br>columns: list, the columns to be analized
<br><br>E.g: <br> <i>list = ['Card Type', 'Issuing Bank', 'Descriptor Name']<br>
x.decline(list)</i>

# approval()
> Top x that are approving more
<br>Args: 
<br>columns: list, the columns to be analized
<br><br>E.g: <br> <i>x.approved()</i>

# specific_approval()
> Returns the approval rate for specific parameters.
<br>Args: 
<br>filter_by: str, column
<br>subfilter (otional): any, value inside the column or empty for column overall numbers
<br><br>E.g: <br> <i>x.specific_approval('Card Type', 'Visa')</i>

# share()
> Returns the share that x represents in the operation (per category)
<br>Args: 
<br>filter_by: str, column
<br>subfilter (otional): any, value inside the column or empty for column overall numbers
<br><br>E.g: <br> <i>x.share('Card Type', 'Visa')</i>

# impact()
> Returns the impact x has on the general operation (per category)
<br>Args: 
<br>filter_by: str, column
<br>subfilter (otional): any, value inside the column or empty for column overall numbers
<br><br>E.g: <br> <i>x.specific_approval('Issuing Bank', 'Visa')</i>

# search()
> Searchs a transaction by its Transaction ID
<br>Args: 
<br>transaction_id: str, the Transaction ID of the transaction
<br><br>E.g: <br> <i>x.search('3g3csshp')</i>

# binBank()
> Returns the Issuing Bank of a BIN
<br>Args: 
<br>bin: int, the BIN to be searched
<br><br>E.g: <br> <i>x.binBank(550209)</i>

# crosstab()
> Crosses two columns inside a dataframe.
<br>Args: 
<br>col1: str, the first column to be used in the cross tabulation.
<br>col2: str, The second column to be used in the cross tabulation.
<br><br>E.g: <br> <i>x.crosstab('Card Type', 'Processor Response Text')</i>

