from app import db, Candidate, app

with app.app_context():
    db.create_all()

    if Candidate.query.count() == 0:
        db.session.add(Candidate(name="Alice"))
        db.session.add(Candidate(name="Bob"))
        db.session.commit()
        print("Database created and candidates added.")
    else:
        print("Candidates already exist.")
