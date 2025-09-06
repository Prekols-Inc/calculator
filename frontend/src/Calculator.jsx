import React, { useState } from "react";
import { calculate, getHistoryStub } from "./API";
import { ToastContainer } from "react-toastify";
import "./styles/Calculator.css";

const error_msg = "Error";

export default function Calculator() {
    const [expression, setExpression] = useState("");
    const [showHistory, setShowHistory] = useState(false);
    const [history, setHistory] = useState([]);

    const buttons = [
        "7", "8", "9", "/",
        "4", "5", "6", "*",
        "1", "2", "3", "-",
        "0", "(", ")",
        "+", ".", "=", "C"
    ];

    const handleClick = async (value) => {
        if (value === "C") {
            setExpression("");
        } else if (value === "=") {
            calculate(expression)
                .then((result) => {
                    setExpression(String(result));
                })
                .catch(() => {
                    setExpression(error_msg);
                });
        } else {
            if (expression === error_msg) {
                setExpression(value);
            } else {
                setExpression(expression + value);
            }
        }
    };

    const openHistory = () => {
        try {
            const data = getHistoryStub();
            setHistory(data);
            setShowHistory(true);
        } catch {
            alert("Failed to load history");
        }
    };

    return (
        <div className="calculator">
            <ToastContainer
                position="top-right"
                autoClose={3000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            />

            <button className="history-btn" onClick={openHistory}>
                History
            </button>

            <div className="calc-wrapper">
                <div className="display">{expression || "0"}</div>
                <div className="buttons">
                    {buttons.map((btn) => (
                        <button
                            key={btn}
                            onClick={() => handleClick(btn)}
                            className={
                                btn === "=" ? "equal" : btn === "C" ? "clear" :
                                    ["/", "*", "-", "+"].includes(btn) ? "operator" : ""
                            }
                        >
                            {btn}
                        </button>
                    ))}
                </div>
            </div>

            {showHistory && (
                <div className="modal">
                    <div className="modal-content history-modal">
                        <h2>History</h2>
                        <div className="history-table-wrapper">
                            <table className="history-table">
                                <thead>
                                    <tr>
                                        <th>Date</th>
                                        <th>Expression</th>
                                        <th>Result</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {history.map((item, idx) => (
                                        <tr key={idx}>
                                            <td>{item.date || new Date().toLocaleString()}</td>
                                            <td>{item.expression}</td>
                                            <td>{item.result}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                        <button onClick={() => setShowHistory(false)}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
}
