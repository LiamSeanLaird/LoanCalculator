import React from 'react';

interface LoanDisplayProps {
    loanData: {
        monthly_payment: string;
        id?: number,
        loan_amount?: string,
        interest_rate?: string,
        loan_term?: string
        customer?: null | object
    };
}

const LoanDisplay: React.FC<LoanDisplayProps> = ({ loanData }) => {
    return (
        <div>
            <h2>Loan Calculation Result</h2>
            <p>Monthly Payment: ${parseFloat(loanData.monthly_payment).toFixed(2)}</p>
        </div>
    );
};

export default LoanDisplay;

