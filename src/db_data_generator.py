"""
Generates sample test data
"""
#pylint: disable=invalid-name
import traceback
from datetime import timedelta
from src.db import DB
import src.random_generator as Random

DOC_TYPE = {
    1: 'Project Document 1',
    2: 'Project Document 2',
    3: 'Proof of Port of Embarkation',
    4: 'PCS Orders',
    5: 'Letter From Medical Provider',
    6: 'Nucleic Acid Amplification Test'
}

IMAGES = ('png', 'jpg')

def _gen_request_id(seq):
    """
    Generates Request ID
    """
    return f'!!{seq:05}'

def _gen_traveler_id(seq1, seq2):
    """
    Generates Traveler ID
    """
    return f'!!{seq1:05}T{seq2:02}'

def _gen_doc_id(seq1, seq2):
    """
    Generates Document ID
    """
    return f'!!{seq1:05}D{seq2:02}'

def _gen_request_file(file_type, seq1, seq2 = 0):
    """
    Generates RequestS File
    """
    rid = _gen_request_id(seq1)
    ext = Random.random_file_type()
    folder = 'Requests_Files_'
    if ext in IMAGES:
        folder = 'Requests_Images'
    return f'{folder}/{rid}.{file_type}.{seq2:04}.{ext}'

def _gen_traveler_file(seq1, seq2):
    """
    Generates Travelers File
    """
    tid = _gen_traveler_id(seq1, seq2)
    ext = Random.random_file_type()
    folder = 'Travelers_Files_'
    if ext in IMAGES:
        folder = 'Travelers_Images'
    return f'{folder}/{tid}.Picuture ID.{seq2:04}.{ext}'

def _gen_doc_file(seq1, seq2):
    """
    Generates Documents File
    """
    docid = _gen_doc_id(seq1, seq2)
    ext = Random.random_file_type()
    folder = 'Documents_Files_'
    if ext in IMAGES:
        folder = 'Documents_Images'
    return f'{folder}/{docid}.File.{seq2:04}.{ext}'

def _gen_dates(base_time, offset, invalid = False):
    """
    Generates created, updated, arrived date
    """
    created = base_time + timedelta(offset)
    updated = created + timedelta(Random.random_number(0, 3))
    arrived = created + timedelta(Random.random_number(-2, 14))
    if invalid:
        val = Random.random_number(0, 2)
        if val == 0:
            arrived = None
        elif val == 1:
            arrived = created + timedelta(Random.random_number(-100, -50))
        else:
            arrived = created + timedelta(Random.random_number(300, 400))
    return {
        'created': created.strftime('%Y-%m-%d'),
        'updated': updated.strftime('%Y-%m-%d'),
        'arrived': arrived.strftime('%Y-%m-%d') if arrived else None
    }

def generate_request(seq, owner, dates):
    """
    Generates Request seed

    OUTPUT

    [
      RequestId,
      UserId,
      Owner,
      Status,
      `Application Confirmation ID`,
      `Request Date`,
      `Approval Date`,
      `Approval ID`,
      `Arrival Date`,
      `Exemption Category`,
      `Project Document 1`,
      `Project Document 2`,
      `Proof of Port of Embarkation`,
      `PCS Orders`,
      `Letter From Medical Provider`,
      `Nucleic Acid Amplification Test`,
      CreatedAt,
      UpdatedAt,
      UpdatedBy
    ]

    """
    rid = _gen_request_id(seq)
    uid = 'TEST'
    status = Random.random_status()
    confirmation_id = rid
    requested = dates['created']
    approval_id = rid if status == 'Approved' else None
    approved = dates['updated'] if status == 'Approved' else None
    arrived = dates['arrived']
    category = Random.random_exemption_category()
    c_at = dates['created']
    u_at = dates['updated']
    u_by = owner
    docs = {}
    for i in range(1, Random.random_number(1, 3) + 1):
        doc_type = Random.random_number(1, 6)
        docs[doc_type] = _gen_request_file(DOC_TYPE[doc_type], seq, i)
    return (rid, uid, owner, status, confirmation_id, requested,
            approved, approval_id, arrived, category,
            docs.get(1), docs.get(2), docs.get(3),
            docs.get(4), docs.get(5), docs.get(6),
            c_at, u_at, u_by)

def generate_traveler(seq1, seq2, owner, dates):
    """
    Generates Traveler seed

    OUTPUT

        [ RequestId, TravelerId, Owner, `First Name`, `Last Name`, `Arrival Date`,
          `Picture ID`, CreatedAt, UpdatedAt, UpdatedBy ]

    """
    rid = _gen_request_id(seq1)
    tid = _gen_traveler_id(seq1, seq2)
    fname = Random.generate_name()
    lname = Random.generate_name()
    adate = dates['arrived']
    pic = _gen_traveler_file(seq1, seq2)
    c_at = dates['created']
    u_at = dates['updated']
    u_by = owner
    return (rid, tid, owner, fname, lname, adate, pic, c_at, u_at, u_by)

def generate_document(seq1, seq2, owner, dates):
    """
    Generates Document seed

    OUTPUT

        [ RequestId, DocumentId, Owner, File,
          CreatedAt, UpdatedAt, UpdatedBy]
    """
    rid = _gen_request_id(seq1)
    docid = _gen_doc_id(seq1, seq2)
    doc = _gen_doc_file(seq1, seq2)
    c_at = dates['created']
    u_at = dates['updated']
    u_by = owner
    return (rid, docid, owner, doc, c_at, u_at, u_by)

def bulk_generate_requests(owner, base_date, days = 5, quantity = 1, offset = 0):
    """
    Generates Request data of the specified number
    """
    data = []
    for i in range(0, days):
        dates = _gen_dates(base_date, i)
        for j in range(1, quantity + 1):
            data.append(generate_request(i * quantity + j + offset, owner, dates))
    return data

def bulk_generate_travelers(owner, base_date, days = 5, quantity = 1, invalid = False, offset = 0):
    """
    Generates Traveler data of the specified number
    """
    data = []
    print(invalid)
    for i in range(0, days):
        dates = _gen_dates(base_date, i, invalid)
        print(dates)
        for j in range(1, quantity + 1):
            for k in range(1, Random.random_number(1, 3) + 1):
                data.append(generate_traveler(i * quantity + j + offset, k, owner, dates))
    return data

def bulk_generate_documents(owner, base_date, days = 5, quantity = 1, offset = 0):
    """
    Generates Document data of the specified number
    """
    data = []
    for i in range(0, days):
        dates = _gen_dates(base_date, i)
        for j in range(1, quantity + 1):
            for k in range(1, Random.random_number(1, 2) + 1):
                data.append(generate_document(i * quantity + j + offset, k, owner, dates))
    return data

def bulk_generate(owner, base_date, days = 5, quantity = 1, invalid = False, offset = 0):
    """
    Generates data of the specified number
    """
    requests = bulk_generate_requests(owner, base_date, days, quantity, offset)
    travelers = bulk_generate_travelers(owner, base_date, days, quantity, invalid, offset)
    docs = bulk_generate_documents(owner, base_date, days, quantity, offset)
    return {
        'requests': requests,
        'travelers': travelers,
        'documents': docs
    }

def populate(conf, owner, base_date, days = 5, quantity = 1, invalid = False, offset = 0):
    """
    Populates Requests, Travelers, Documents tables with randomly geneated data
    """
    try:
        data = bulk_generate(owner, base_date, days, quantity, invalid, offset)
        db = DB(conf)
        rslt = db.insert_requests(data['requests'])
        print(rslt)
        rslt = db.insert_travelers(data['travelers'])
        print(rslt)
        rslt = db.insert_documents(data['documents'])
        print(rslt)
        db.close()
    except Exception as err:
        traceback.print_exc()
        print(err)

def delete_all(conf):
    """
    Delete test data
    """
    SQL1 = "DELETE FROM Travelers WHERE RequestId LIKE '!!%'"
    SQL2 = "DELETE FROM Documents WHERE RequestId LIKE '!!%'"
    SQL3 = "DELETE FROM Requests WHERE RequestId LIKE '!!%'"
    SQL4 = "DELETE FROM ArchivedFiles WHERE RequestId LIKE '!!%'"
    SQL5 = "DELETE FROM ArchivedRequests WHERE RequestId LIKE '!!%'"
    try:
        db = DB(conf)
        rslt = db.exec(SQL1)
        print(f'{rslt} Travelers Deleted')
        rslt = db.exec(SQL2)
        print(f'{rslt} Documents Deleted')
        rslt = db.exec(SQL3)
        print(f'{rslt} Requests Deleted')
        rslt = db.exec(SQL4)
        print(f'{rslt} ArchivedFiles Deleted')
        rslt = db.exec(SQL5)
        print(f'{rslt} ArchivedRequests Deleted')
        db.close()
    except Exception as err:
        traceback.print_exc()
        print(err)

def query(conf, sql):
    """
    Executes the given query
    """
    rslt = None
    try:
        db = DB(conf)
        rslt = db.query(sql)
        print(rslt)
        db.close()
    except Exception as err:
        traceback.print_exc()
        print(err)
    return rslt
